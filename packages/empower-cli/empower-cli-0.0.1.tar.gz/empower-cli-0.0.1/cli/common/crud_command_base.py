import json
from abc import ABC
from typing import Optional, Union
from urllib.parse import urlencode

import requests
import typer
from cli.common.auth.manager import CLIAuthManager
from cli.common.enums import RequestMethods
from cli.common.service_type import ServiceType
from cli.common.util import get_request_url
from requests.sessions import Session


class CRUDCommandBase(ABC):
    def __init__(self, service_type: ServiceType, endpoint: str) -> None:
        self.service_type = service_type
        self.endpoint = endpoint
        self.auth_manager = CLIAuthManager()

    def create(self, data: str = None) -> str:
        """Make a POST request to an API endpoint with either JSON data
        or a path to the JSON file provided.

        :param data: JSON data
        :raises BadParameter:
            Neither JSON data or JSON file path has been provided
        :return: serialized response data
        """
        self._guard_input(data)
        url: str = f"{get_request_url(self.service_type)}/{self.endpoint}"
        json_data = self._convert_to_j_object_list(data)

        created = [
            self._make_request(RequestMethods.POST, url, data=json.dumps(item)).json()
            for item in json_data
        ]
        return json.dumps(created, indent=2)

    def update(self, data: Optional[str] = None) -> str:
        """Make a PUT request to an API endpoint with either JSON data
        or a path to the JSON file provided.

        :param data: JSON data
        :raises BadParameter:
            Neither JSON data or JSON file path has been provided
        :return: serialized response data
        """
        self._guard_input(data)
        url: str = f"{get_request_url(self.service_type)}/{self.endpoint}"
        json_data = self._convert_to_j_object_list(data)

        created = [
            self._make_request(RequestMethods.PUT, url, data=json.dumps(item)).json()
            for item in json_data
        ]
        return json.dumps(created, indent=2)

    def get(self) -> str:
        """Make a GET request to the API.

        :return: serialized response data.
        """
        url = self.default_url(self.endpoint)
        response = self._make_request(RequestMethods.GET, url)
        typer.echo(f"request made to: {url}")
        return json.dumps(response.json(), indent=2)

    def get_by_id(self, id_: Union[str, dict]) -> str:
        """
        Make a GET request to the api endpoint to retrieve the
        object with the provided id

        :param id_: the object id
        :return: serialized response data
        """
        self._guard_input(id_)
        if isinstance(id_, str):
            url = f"{self.default_url(self.endpoint)}/{id_}"
        if isinstance(id_, dict):
            url = f"{self.default_url(self.endpoint)}/?{urlencode(id_)}"

        response = self._make_request(RequestMethods.GET, url)
        typer.echo(f"request made to: {url}")

        return json.dumps(response.json(), indent=2)

    # todo: might have to modify this to support composite primary keys
    def delete(self, id_: Union[str, dict]) -> None:
        """
        Make a DELETE request to the api endpoint with the provided id

        :param id_: the object id
        :return: None
        """
        self._guard_input(id_)
        if isinstance(id_, str):
            url = f"{self.default_url(self.endpoint)}/{id_}"
        if isinstance(id_, dict):
            url = f"{self.default_url(self.endpoint)}/?{urlencode(id_)}"
        self._make_request(RequestMethods.DELETE, url)
        typer.echo(f'{self.endpoint} object with id: "{id_}" successfully deleted')

    def default_url(self, endpoint: str) -> str:
        """Get default URI for the HTTP request with given resource string.

        :param endpoint: URI resource string
        :return: URI for given request resource
        """
        return f"{get_request_url(self.service_type)}/{endpoint}"

    @staticmethod
    def _convert_to_j_object_list(data: str) -> list[str]:
        """Convert JSON object(s) string to a list of JSON object(s).

        :param data: JSON data string.
        :return: list of JSON object(s) string(s)
        """
        json_data = json.loads(data)
        return [json_data] if not isinstance(json_data, list) else json_data

    @staticmethod
    def _guard_input(data: Optional[str]) -> None:
        """Check if data is provided.

        :param data: JSON data string
        :raises BadParameter: Neither JSON data or file were provided.
        """
        if data is None:
            raise typer.BadParameter(
                "No data was provided for this command. "
                "Either provide data or path to the file."
            )

    def _make_request(
        self, method: RequestMethods, url: str, auth_required: bool = True, **kwargs
    ) -> requests.Response:
        """Make a request with a given HTTP method to a given URL.
        Named arguments are the same as for ``requests.sessions.Session.request``.

        :param method: HTTP request method. RequestMethods enum
        :param url: URL to make a request to
        :param auth_required:
        flag that indicates whether to add auth header to a request
        :raises AttributeError: invalid HTTP method
        :return: response data
        """
        # Initialize request headers and extend them with auth headers if required.
        headers = kwargs.pop("headers", {})
        if auth_required:
            headers.update(self.auth_manager.token_auth_header)

        # Make a request with provided parameters and raise for the status
        with Session() as session:
            response: requests.Response = session.request(
                method, url, headers=headers, **kwargs
            )
            response.raise_for_status()

        return response
