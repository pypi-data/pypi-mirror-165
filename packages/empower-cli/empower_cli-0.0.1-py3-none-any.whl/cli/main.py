import typer
from cli.commands import context
from cli.commands.auth import login
from cli.commands.empower_api import empower_api_typer
from cli.commands.empower_discovery import discovery_typer

app = typer.Typer()
app.add_typer(context.app, name="context")
app.add_typer(login.app, name="auth")
app.add_typer(discovery_typer, name="discovery")
app.add_typer(empower_api_typer, name="api")


if __name__ == "__main__":
    app()
