from typing import Optional

import typer

from cli.common.command_help import CRUD_FILE_PATH_HELP
from cli.common.command_util import handle_request_command
from cli.common.crud_command_base import CRUDCommandBase
from cli.common.service_type import ServiceType
from cli.common.util import get_json_data

app = typer.Typer()


class CompanyCRUD(CRUDCommandBase):
    def __init__(
        self,
        service_type: ServiceType = ServiceType.EMPOWER_API,
        endpoint: str = "company",
    ) -> None:
        super().__init__(service_type, endpoint)


@app.command("list")
@handle_request_command
def list_():
    typer.echo(CompanyCRUD().get())


@app.command()
@handle_request_command
def show(
    id_: str = typer.Argument(
        ..., metavar="Company ID", help="A unique identifier for the company."
    )
):
    typer.echo(CompanyCRUD().get_by_id(id_))


@app.command()
@handle_request_command
def create(
    json_: Optional[str] = typer.Option(None, "--json"),
    file_path: Optional[typer.FileText] = typer.Option(
        None,
        mode="r",
        encoding="utf-8",
        callback=get_json_data,
        help=CRUD_FILE_PATH_HELP,
    ),
):
    typer.echo(CompanyCRUD().create(json_ or file_path))
