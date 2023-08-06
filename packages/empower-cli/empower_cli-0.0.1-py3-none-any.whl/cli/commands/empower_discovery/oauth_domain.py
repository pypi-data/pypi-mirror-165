# from typing import Optional
#
# import requests
# import typer
#
# from commands.empower_discovery.endpoint_mapping import map_resource_to_endpoint
# from common.crud_command_base import CRUDCommandBase
# from common.service_type import ServiceType
# from common.util import get_json_data
#
# app = typer.Typer()
# DiscoveryCRUD = CRUDCommandBase(ServiceType.EMPOWER_DISCOVERY)
#
#
# @app.command()
# def show(
#         resource: str,
#         id: str
# ):
#     endpoint = map_resource_to_endpoint(resource)
#
#     try:
#         response = DiscoveryCRUD.get_by_id(endpoint, id)
#     except requests.HTTPError as e:
#         typer.echo(f"Error occurred while retrieving data: {str(e)}")
#         typer.Abort(1)
#     else:
#         typer.echo(response)
#
#
# # todo: allow to take key value pairs as query parameters
# @app.command()
# def list(
#         resource: str
# ):
#     endpoint = map_resource_to_endpoint(resource)
#     handle_crud_command(lambda: DiscoveryCRUD.get(endpoint))
#
#
# @app.command()
# def create(
#         resource: str,
#         json_: Optional[str] = typer.Option(None, "--json"),
#         json_path: Optional[typer.FileText] = typer.Option(
#             None,
#             mode="r",
#             encoding="utf-8",
#             callback=get_json_data,
#         ),
# ):
#     endpoint = map_resource_to_endpoint(resource)
#
#     try:
#         response = DiscoveryCRUD.create(endpoint, json_ or json_path)
#     except requests.HTTPError as e:
#         typer.echo(f"Error occurred while creating data: {str(e)}")
#         typer.Abort(1)
#     else:
#         typer.echo(response)
#
#
# # update not available for oauth-domain
#
# @app.command()
# def delete(
#         resource: str,
#         id: str
# ):
#     endpoint = map_resource_to_endpoint(resource)
#     handle_crud_command(lambda: DiscoveryCRUD.delete(endpoint, id))
#
#
# def handle_crud_command(callback):
#     try:
#         response = callback()
#     except requests.HTTPError as e:
#         typer.echo(f"Error occurred while making request: {str(e)}")
#         typer.Abort(1)
#     else:
#         typer.echo(response)
