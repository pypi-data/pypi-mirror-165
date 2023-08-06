import os

import requests
from cli.common.file_utils import write_credentials_to_json

from .config import PIPELINE_FLOW_CREDENTIALS_FILE, TOKEN_REQUEST_URL


def credentials_flow_auth(
    file_name: str = PIPELINE_FLOW_CREDENTIALS_FILE,
) -> None:
    """
    Get keycloak client credentials.

    :param file_name: credentials storage file name
    :return: keycloak client credentials json
    """
    params = {
        "client_id": os.getenv("EMPOWER_CLI_CLIENT_ID"),
        "client_secret": os.getenv("EMPOWER_CLI_CLIENT_SECRET"),
        "grant_type": "client_credentials",
    }
    credentials = requests.post(TOKEN_REQUEST_URL, data=params).json()
    write_credentials_to_json(credentials, file_name)
