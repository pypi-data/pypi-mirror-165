from typing import Optional

import typer
from cli.common.command_help import CRUD_FILE_PATH_HELP
from cli.common.command_util import handle_request_command
from cli.common.crud_command_base import CRUDCommandBase
from cli.common.service_type import ServiceType
from cli.common.util import get_json_data

app = typer.Typer()


class EnvironmentDatabricksCRUD(CRUDCommandBase):
    def __init__(
        self,
        service_type: ServiceType = ServiceType.EMPOWER_API,
        endpoint: str = "environment/databricks",
    ) -> None:
        super().__init__(service_type, endpoint)


@app.command("list")
@handle_request_command
def list_():
    typer.echo(EnvironmentDatabricksCRUD().get())


@app.command()
@handle_request_command
def show(
    cluster_id: str = typer.Argument(
        ...,
        metavar="Cluster ID",
        help="A surrogate key for the Name:Identifier pair",
    )
):
    typer.echo(EnvironmentDatabricksCRUD().get_by_id(cluster_id))


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
    typer.echo(EnvironmentDatabricksCRUD().create(json_ or file_path))


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
    typer.echo(EnvironmentDatabricksCRUD().update(json_ or file_path))


@app.command()
@handle_request_command
def delete(
    cluster_id: str = typer.Argument(
        ...,
        metavar="Cluster ID",
        help="A surrogate key for the Name:Identifier pair",
    )
):
    typer.echo(EnvironmentDatabricksCRUD().delete(cluster_id))
