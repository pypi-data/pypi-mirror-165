import json
import os
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv

from cli.common.auth.config import BROWSER_FLOW_CREDENTIALS_FILE
from cli.common.auth.parse_token import get_user_info
from cli.common.file_utils import read_credentials_from_json
from cli.common.store_client import store, container_names

app = typer.Typer()


@app.command()
def show():
    _all = store.get_all(container_names.environment)
    token = read_credentials_from_json(BROWSER_FLOW_CREDENTIALS_FILE).get(
        "access_token"
    )
    _all.update(get_user_info(token))
    environment_context = json.dumps(_all, indent=2)
    typer.echo(environment_context)


@app.command("set")
def set_(
    api_url: str = typer.Option(
        None, help="Url for the main empower api. Must be set prior to 'empower login'"
    ),
    discovery_url: str = typer.Option(
        None, help="Url for the empower discovery service."
    ),
    licensing_url: str = typer.Option(
        None, help="Url for the empower licensing service."
    ),
    env_path: Optional[Path] = typer.Option(
        None,
        help="Relative or full path to optional .env file with context values.",
        resolve_path=True,
        exists=True,
    ),
):
    typer.echo(env_path)
    if env_path is not None:
        load_dotenv(dotenv_path=env_path)
        empower_api_url: str = os.environ.get("API_URL")
        empower_discovery_url: str = os.environ.get("DISCOVERY_URL")
        empower_licensing_url: str = os.environ.get("LICENSING_URL")

    if api_url is not None:
        empower_api_url = api_url

    if api_url is not None:
        empower_discovery_url = discovery_url

    if licensing_url is not None:
        empower_licensing_url = licensing_url

    store.empower_api_url = empower_api_url
    store.empower_discovery_url = empower_discovery_url
    store.empower_licensing_url = empower_licensing_url


# # set empower api domain
# @app.command()
# def empower_api_domain(domain: str):
#     context.empower_api_domain = domain
#
#
# # set discovery service domain
# @app.command()
# def empower_api_domain(domain: str):
#     context.discovery_api_domain = domain
#
#
# # set ssl value to true or false
# @app.command()
# def ssl(value: str):
#     setting = pydantic.parse_obj_as(bool, value.lower())
#     context.ssl = setting
