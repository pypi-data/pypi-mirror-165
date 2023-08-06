import typer

from cli.common.crud_command_base import CRUDCommandBase
from cli.common.service_type import ServiceType

app = typer.Typer()
DiscoveryCRUD = CRUDCommandBase(ServiceType.EMPOWER_DISCOVERY)
DEFAULT_ENDPOINT = "auth-url"

app.command(
    help="retrieve the auth url configuration associated with the provided domain"
)


def show(domain: str):
    endpoint = f"auth-url/{domain}"
    return typer.echo(DiscoveryCRUD.get(endpoint))
