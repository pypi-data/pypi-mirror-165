import datetime
import json
from pathlib import Path
from typing import Any, Union

import requests
from cli.common.file_utils import read_credentials_from_json, write_credentials_to_json
from jose import ExpiredSignatureError

from .config import (
    ACCESS_TOKEN_EXP_TIMEDELTA,
    BROWSER_FLOW_CREDENTIALS_FILE,
    TOKEN_REFRESH_URL,
    keycloak_openid,
)


class CLIAuthManager:
    def __init__(
        self,
        credentials_file_name: Union[str, Path] = BROWSER_FLOW_CREDENTIALS_FILE,
    ) -> None:
        self.credentials_file_name = credentials_file_name

    def get_auth_credentials(self) -> str:
        """Get auth access token string from local credentials file.

        :raises ValueError: access token not in the local credentials file
        :return: access token string
        """
        credentials = read_credentials_from_json(self.credentials_file_name)
        access_token = credentials.get("access_token", None)
        if access_token is None:
            raise ValueError("Unable to obtain auth credentials data. Login again.")

        return credentials

    @property
    def access_token(self) -> str:
        """Get access token string value from credentials file.

        :return: access token string
        """
        return self.get_auth_credentials().get("access_token")

    @property
    def token_auth_header(self) -> dict[str, str]:
        """Get auth header dictionary for the HTTP request.

        :return: auth header dictionary
        """
        if self._token_expired():
            self.refresh_credentials()
        return {"Authorization": f"Bearer {self.access_token}"}

    def refresh_credentials(self) -> None:
        """Refresh auth credentials using refresh token.

        :return: None
        """
        refresh_token = self.get_auth_credentials().get("refresh_token")
        refreshed_credentials = requests.post(
            TOKEN_REFRESH_URL, data=json.dumps({"refresh_token": refresh_token})
        )
        write_credentials_to_json(
            refreshed_credentials.json(), self.credentials_file_name
        )

    def __decode_access_token(self) -> dict[str, Any]:
        """Decode access token.

        :return: decoded access token info dictionary
        """
        return keycloak_openid.decode_token(
            self.access_token,
            "",
            options={"verify_signature": False, "verify_aud": False},
        )

    def _token_expired(self) -> bool:
        """Check if access token expired."""
        try:
            token_decoded = int(self.__decode_access_token().get("exp"))
        except ExpiredSignatureError:
            return True

        exp_timestamp = datetime.datetime.fromtimestamp(token_decoded)
        timedelta: datetime.timedelta = datetime.datetime.utcnow() - exp_timestamp
        return timedelta.seconds < ACCESS_TOKEN_EXP_TIMEDELTA
