from functools import wraps
from typing import Any, Callable

import requests
import typer


def handle_request_command(func: Callable[..., Any]) -> Callable[..., Any]:
    """Process typer command, catch errors if any occurred."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            # Call a request func
            result: requests.Response = func(*args, **kwargs)
        except requests.HTTPError as e:
            typer.echo(str(e))
            typer.Abort(1)
        except requests.exceptions.ConnectionError as e:
            typer.echo(
                f"{e.__class__.__name__}: "
                "Counld not establish connection to the server."
            )
            typer.Abort(1)
        else:
            return result

    return wrapper
