from cli.common.auth.server import AuthCodeReceiver

from .config import BROWSER_LOGIN_URL, HOST_NAME, PORT


def browser_auth() -> None:
    """
    CLI login with a keycloak browser form.

    :return: None
    """
    with AuthCodeReceiver(host=HOST_NAME, port=PORT) as receiver:
        receiver.get_auth_response(
            auth_uri=BROWSER_LOGIN_URL,
            timeout=60,
        )
