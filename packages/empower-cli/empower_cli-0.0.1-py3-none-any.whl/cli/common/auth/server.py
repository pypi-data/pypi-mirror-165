import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

import requests
from cli.common.auth.config import (
    AUTH_EXCHANGE_URL,
    BROWSER_FLOW_CREDENTIALS_FILE,
    REDIRECT_URI,
)
from cli.common.file_utils import write_credentials_to_json


def is_wsl() -> bool:
    """Check if client uses WSL.

    :return: bool
    """
    import platform

    uname = platform.uname()
    platform_name = getattr(uname, "system", uname[0]).lower()
    release = getattr(uname, "release", uname[2]).lower()
    return platform_name == "linux" and "microsoft" in release


def _browse(auth_uri: str, browser_name: str = None) -> bool:
    """Browse uri with named browser.

    :param auth_uri: auth server uri
    :param browser_name: browser system name, defaults to None
    :return: boolean flag indicating whether browser has opened
    """
    import webbrowser

    if browser_name:
        browser_opened = webbrowser.get(browser_name).open(auth_uri)
    else:
        browser_opened = webbrowser.open(auth_uri)

    if not browser_opened and is_wsl():
        try:
            import subprocess

            exit_code = subprocess.call(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-Command",
                    f'Start-Process "{auth_uri}"',
                ]
            )
            browser_opened = exit_code == 0
        except FileNotFoundError:
            pass
    return browser_opened


class _AuthCodeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get query parameters dict
        query_params = dict(parse_qsl(urlparse(self.path).query))
        self.server.auth_response = query_params
        message = (
            self.server.success_template
            if "code" in query_params
            else self.server.error_template
        )
        self._send_full_response(message)

    def _send_full_response(self, body, is_ok=True):
        self.send_response(200 if is_ok else 400)
        self.send_header(
            "Content-type",
            "text/html" if body.startswith("<") else "text/plain",
        )
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, format: str, *args) -> None:
        return


class _AuthCodeHttpServer(HTTPServer):
    def __init__(self, server_address, *args, **kwargs):
        _, port = server_address
        if port and (sys.platform == "win32" or is_wsl()):
            # The default allow_reuse_address is True. It works fine on non-Windows.
            # On Windows, it undesirably allows multiple servers listening on same port,
            # yet the second server would not receive any incoming request,
            # so it should be turned off.
            self.allow_reuse_address = False
        super().__init__(server_address, *args, **kwargs)

    def handle_timeout(self):
        """Terminate the server on timeout."""
        raise RuntimeError("Timeout. No auth response arrived.")


class AuthCodeReceiver:
    def __init__(self, host: str, port: int = None) -> None:
        """Create a Receiver waiting for incoming auth response.

        :param port:
            The local web server will listen at http://...:<port>
        """
        self._server = _AuthCodeHttpServer((host, port or 0), _AuthCodeHandler)
        self._closing = False

    def get_auth_response(self, timeout: int = None, **kwargs) -> None:
        """Wait and return the auth response. Raise RuntimeError when timeout.

        :param str auth_uri:
            If provided, this function will try to open a local browser.
        :param int timeout: In seconds. None means wait indefinitely.
        :param str browser_name:
            If you did
            ``webbrowser.register("xyz", None, BackgroundBrowser("/path/to/browser"))``
            beforehand, you can pass in the name "xyz" to use that browser.
            The default value ``None`` means using default browser,
            which is customizable by env var $BROWSER.
        :return:
            The auth response of the first leg of Auth Code flow,
            typically {"code": "...", "state": "..."} or {"error": "...", ...}
            Returns None when the state was mismatched, or when timeout occurred.
        """
        thread = threading.Thread(target=self._get_auth_response, kwargs=kwargs)
        thread.daemon = True
        thread.start()

        begin = time.time()
        while ((time.time() - begin) < int(timeout)) if timeout else True:
            time.sleep(1)
            if not thread.is_alive():
                break

    def _get_auth_response(
        self,
        auth_uri: str = None,
        timeout: int = None,
        browser_name: str = None,
    ) -> None:
        browser_opened = False
        try:
            browser_opened = _browse(auth_uri, browser_name=browser_name)
        except Exception as e:
            raise Exception("_browse(...) unsuccessful") from e

        if not browser_opened:
            print("Found no browser in current environment.")

        self._server.success_template = (
            "Authentication completed. You can close this window now."
        )
        self._server.error_template = "Authentication failed."

        self._server.timeout = timeout
        self._server.auth_response = {}

        while not self._closing:
            # Handle keycloak callback
            self._server.handle_request()
            # Get auth code
            code = self._server.auth_response.get("code")
            # Get auth credentials via API exchange url request with recieved code
            self.parse_auth_credentials(code)
            self.close()

    @staticmethod
    def parse_auth_credentials(code: str) -> str:
        """
        Send a /auth/exchange request to the API with received code and redirect URI.

        :param code: access_code form keycloak.
        :return: JWT access token
        """
        credentials = requests.get(
            AUTH_EXCHANGE_URL,
            params={"code": code, "redirect_uri": REDIRECT_URI},
        ).json()
        if credentials is None or "access_token" not in credentials:
            raise ValueError("Unable to obtain the authentication credentials.")
        write_credentials_to_json(
            credentials=credentials, file_name=BROWSER_FLOW_CREDENTIALS_FILE
        )
        return credentials

    def close(self) -> None:
        """Close an HTTP server."""
        self._closing = True
        self._server.server_close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
