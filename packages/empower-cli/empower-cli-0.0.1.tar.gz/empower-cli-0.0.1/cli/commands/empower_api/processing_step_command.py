from typing import Optional

import typer
from cli.common.command_help import CRUD_FILE_PATH_HELP
from cli.common.command_util import handle_request_command
from cli.common.crud_command_base import CRUDCommandBase
from cli.common.service_type import ServiceType
from cli.common.util import get_json_data

app = typer.Typer()


class ProcessingStepCommandCRUD(CRUDCommandBase):
    def __init__(
        self,
        service_type: ServiceType = ServiceType.EMPOWER_API,
        endpoint: str = "processing-step",
    ) -> None:
        super().__init__(service_type, endpoint)


@app.command("list")
@handle_request_command
def list_():
    typer.echo(ProcessingStepCommandCRUD().get())


@app.command()
@handle_request_command
def show(
    command_id: str = typer.Argument(
        ..., metavar="Command ID", help="A surrogate key for the object"
    )
):
    typer.echo(ProcessingStepCommandCRUD().get_by_id(command_id))


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
    typer.echo(ProcessingStepCommandCRUD().create(json_ or file_path))


@app.command()
@handle_request_command
def update(
    json_: Optional[str] = typer.Option(None, "--json"),
    file_path: Optional[typer.FileText] = typer.Option(
        None,
        mode="r",
        encoding="utf-8",
        callback=get_json_data,
        help=CRUD_FILE_PATH_HELP,
    ),
):
    typer.echo(ProcessingStepCommandCRUD().update(json_ or file_path))


@app.command()
@handle_request_command
def delete(
    command_id: str = typer.Argument(
        ..., metavar="Command ID", help="A surrogate key for the object"
    )
):
    typer.echo(ProcessingStepCommandCRUD().delete(command_id))
