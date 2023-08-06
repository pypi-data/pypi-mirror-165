import typer
from cli.commands.empower_discovery import enterprise

discovery_typer = typer.Typer()

discovery_typer.add_typer(enterprise.app, name="enterprise")
