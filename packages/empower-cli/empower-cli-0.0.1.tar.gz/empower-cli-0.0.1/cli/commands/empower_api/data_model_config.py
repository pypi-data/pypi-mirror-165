from typing import Optional

import typer

from cli.common.command_help import CRUD_FILE_PATH_HELP
from cli.common.command_util import handle_request_command
from cli.common.crud_command_base import CRUDCommandBase
from cli.common.service_type import ServiceType
from cli.common.util import get_json_data

app = typer.Typer()


class DataModelConfigCRUD(CRUDCommandBase):
    def __init__(
        self,
        service_type: ServiceType = ServiceType.EMPOWER_API,
        endpoint: str = "data-model-config",
    ) -> None:
        super().__init__(service_type, endpoint)


@app.command("list")
@handle_request_command
def list_():
    typer.echo(DataModelConfigCRUD().get())


@app.command()
@handle_request_command
def show(
    model_name: str = typer.Option(..., "--model"),
    target_schema_name: str = typer.Option(..., "--schema"),
    target_table_name: str = typer.Option(..., "--table"),
    target_column_name: str = typer.Option(..., "--column"),
):
    typer.echo(
        DataModelConfigCRUD().get_by_id(
            dict(
                model_name=model_name,
                target_schema_name=target_schema_name,
                target_column_name=target_column_name,
                target_table_name=target_table_name,
            )
        )
    )


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
    typer.echo(DataModelConfigCRUD().create(json_ or file_path))


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
    typer.echo(DataModelConfigCRUD().update(json_ or file_path))


@app.command()
@handle_request_command
def delete(
    model_name: str = typer.Option(..., "--model"),
    target_schema_name: str = typer.Option(..., "--schema"),
    target_table_name: str = typer.Option(..., "--table"),
    target_column_name: str = typer.Option(..., "--column"),
):
    typer.echo(
        DataModelConfigCRUD().delete(
            dict(
                model_name=model_name,
                target_schema_name=target_schema_name,
                target_column_name=target_column_name,
                target_table_name=target_table_name,
            )
        )
    )
