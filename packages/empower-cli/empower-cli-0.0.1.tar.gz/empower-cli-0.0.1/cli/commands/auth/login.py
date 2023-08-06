import requests
import typer

from cli.common.auth import credentials_flow_auth
from cli.common.service_type import ServiceType

app = typer.Typer()
ENDPOINT = "auth"
SERVICE_TYPE = ServiceType.EMPOWER_AUTH


@app.command(help="Login user within an opened browser tab.")
def login() -> None:
    typer.echo("Processing login. Wait for the browser window to open.")

    try:
        browser_auth()
    except ValueError as e:
        typer.echo(f"Authentication error: {e}")
    except RuntimeError as e:
        typer.echo(e)
    else:
        typer.echo("Logged in successfully.")


@app.command(help="Pipeline authentication using 'client_credentials' flow.")
def login_pipeline() -> None:
    typer.echo("Processing login.")
    try:
        credentials_flow_auth()
    except requests.HTTPError:
        typer.echo("Error occurred while getting authentication credentials.")
        typer.Abort(1)
    else:
        typer.echo("Logged in successfully.")
