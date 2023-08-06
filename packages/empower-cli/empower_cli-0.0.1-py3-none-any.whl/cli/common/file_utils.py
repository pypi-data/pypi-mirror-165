import json
from pathlib import Path
from typing import Union

from cli.common.auth.config import CREDENTIALS_FILE_PATH


def write_credentials_to_json(credentials: str, file_name: Union[str, Path]) -> None:
    """
    Write client credentials to json file.

    :param credentials: keycloak client credentials json
    :param file_name: credentials storage file name
    :return: None
    """
    with open(CREDENTIALS_FILE_PATH / file_name, "w", encoding="utf-8") as file:
        json.dump(credentials, file, indent=4, ensure_ascii=True)


def read_credentials_from_json(file_name: Union[str, Path]) -> dict:
    """
    Read client credentials from json file.

    :param file_name: credentials storage file name
    :return: client credentials dict
    """
    with open(CREDENTIALS_FILE_PATH / file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
