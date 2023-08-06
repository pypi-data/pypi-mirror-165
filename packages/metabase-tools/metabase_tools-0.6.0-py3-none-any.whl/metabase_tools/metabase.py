"""
Rest adapter for the Metabase API
"""
from __future__ import annotations  # Included for support of |

import logging
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Optional

from requests import Response, Session
from requests.exceptions import RequestException

from metabase_tools.exceptions import (
    AuthenticationFailure,
    InvalidDataReceived,
    RequestFailure,
)


class MetabaseApi:
    """Metabase API adapter"""

    def __init__(
        self,
        metabase_url: str,
        credentials: Optional[dict[str, str]] = None,
        cache_token: bool = False,
        token_path: Optional[Path | str] = None,
    ):
        self._logger = logging.getLogger(__name__)
        if not credentials and not token_path:
            raise AuthenticationFailure("No authentication method provided")
        credentials = credentials or {}
        token_path = Path(token_path) if token_path else None

        # Validate Metabase URL
        self.metabase_url = self._validate_base_url(url=metabase_url)

        # Starts session to be reused by the adapter so that the auth token is cached
        self._session = Session()

        # Authenticate
        self._authenticate(token_path=token_path, credentials=credentials)

        if cache_token:
            save_path = Path(token_path or "metabase.token")
            self.save_token(save_path=save_path)

    def _validate_base_url(self, url: str) -> str:
        if url[-1] == "/":
            url = url[:-1]
        if url[-4:] == "/api":
            url = url[:-4]
        if url[:4] != "http":
            url = f"http://{url}"
        return f"{url}/api"

    def _authenticate(
        self, token_path: Optional[Path], credentials: dict[str, str]
    ) -> None:
        authed = False
        # Try cached token first
        if token_path and token_path.exists():
            authed = self._auth_with_cached_token(token_path=token_path)
            if not authed:
                self._delete_cached_token(token_path=token_path)
        # Try token passed as credentials next
        if not authed and "token" in credentials:
            authed = self._auth_with_passed_token(credentials=credentials)
        # Finally try username and password
        if not authed and "username" in credentials and "password" in credentials:
            authed = self._auth_with_login(credentials=credentials)
        # Raise error if still not authenticated
        if not authed:
            self._logger.error("Failed to authenticate")
            raise AuthenticationFailure(
                "Failed to authenticate with credentials provided"
            )

    def _add_token_to_header(self, token: str) -> None:
        headers = {
            "Content-Type": "application/json",
            "X-Metabase-Session": token,
        }
        self._session.headers.update(headers)

    def _delete_cached_token(self, token_path: Path) -> None:
        if token_path.exists():
            self._logger.warning("Deleting token file")
            token_path.unlink()

    def _auth_with_cached_token(self, token_path: Path) -> bool:
        with open(token_path, "r", encoding="utf-8") as file:
            token = file.read()
        self._logger.debug("Attempting authentication with token file")
        self._add_token_to_header(token=token)
        authed = self.test_for_auth()
        self._logger.debug(
            "Authenticated with token file"
            if authed
            else "Failed to authenticate with token file"
        )
        return authed

    def _auth_with_passed_token(self, credentials: dict[str, str]) -> bool:
        self._logger.debug("Attempting authentication with token passed")
        self._add_token_to_header(token=credentials["token"])
        authed = self.test_for_auth()
        self._logger.debug(
            "Authenticated with token passed"
            if authed
            else "Failed to authenticate with token passed"
        )
        return authed

    def _auth_with_login(self, credentials: dict[str, str]) -> bool:
        """Private method for authenticating a session with the API

        Args:
            credentials (dict): Username and password
        """
        try:
            self._logger.debug("Attempting authentication with username and password")
            response = self._session.post(
                f"{self.metabase_url}/session", json=credentials
            )
            self._add_token_to_header(token=response.json()["id"])
            authed = self.test_for_auth()
            self._logger.debug(
                "Authenticated with login"
                if authed
                else "Failed to authenticate with login"
            )
            return authed
        except KeyError as error_raised:
            self._logger.warning(
                "Exception encountered during attempt to authenticate with login \
                    passed: %s",
                error_raised,
            )
        return False

    def test_for_auth(self) -> bool:
        """Validates successful authentication by attempting to retrieve data about \
            the current user

        Returns:
            bool: Successful authentication
        """
        return (
            200
            <= self._session.get(f"{self.metabase_url}/user/current").status_code
            <= 299
        )

    def save_token(self, save_path: Path | str) -> None:
        """Writes active token to the specified file

        Args:
            save_path (Path | str): Name of file to write
        """
        token = str(self._session.headers.get("X-Metabase-Session"))
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(token)

    def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Response:
        """Perform an HTTP request, catching and re-raising any exceptions

        Args:
            method (str): GET or POST or DELETE or PUT
            url (str): URL endpoint
            params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Raises:
            RequestFailure: Request failed

        Returns:
            Response: Response from the API
        """
        log_line_pre = f"{method=}, {url=}, {params=}"
        try:
            self._logger.debug(log_line_pre)
            return self._session.request(
                method=method, url=url, params=params, json=json
            )
        except RequestException as error_raised:
            self._logger.error(str(error_raised))
            raise RequestFailure("Request failed") from error_raised

    def generic_request(
        self,
        http_method: str,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Method for dispatching HTTP requests

        Args:
            http_method (str): GET or POST or PUT or DELETE
            endpoint (str): URL endpoint
            params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Raises:
            InvalidDataReceived: Unable to decode response from API
            AuthenticationFailure: Auth failure received from API
            RequestFailure: Other failure during request

        Returns:
            list[dict[str, Any]] | dict[str, Any]: Response from API
        """
        log_line_post = "success=%s, status_code=%s, message=%s"
        response = self._make_request(
            method=http_method,
            url=self.metabase_url + endpoint,
            params=params,
            json=json,
        )

        # If status_code in 200-299 range, return Result, else raise exception
        is_success = 299 >= response.status_code >= 200
        if is_success:
            self._logger.debug(
                log_line_post, is_success, response.status_code, response.reason
            )
            try:
                return_ = response.json()
                if isinstance(return_, (list, dict)):
                    return return_
            except JSONDecodeError as error_raised:
                raise InvalidDataReceived from error_raised
        elif response.status_code == 401:
            self._logger.error(
                log_line_post, False, response.status_code, response.text
            )
            raise AuthenticationFailure(f"{response.status_code} - {response.reason}")

        error_line = f"{response.status_code} - {response.reason}"
        self._logger.error(log_line_post)
        raise RequestFailure(error_line)

    def get(
        self, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """HTTP GET request

        Args:
            endpoint (str): URL endpoint
            ep_params (dict, optional): Endpoint parameters

        Returns:
            list[dict[str, Any]] | dict[str, Any]: Response from API
        """
        return self.generic_request(http_method="GET", endpoint=endpoint, params=params)

    def post(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """HTTP POST request

        Args:
            endpoint (str): URL endpoint
            params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Returns:
            list[dict[str, Any]] | dict[str, Any]: Response from API
        """
        return self.generic_request(
            http_method="POST", endpoint=endpoint, params=params, json=json
        )

    def delete(
        self, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """HTTP DELETE request

        Args:
            endpoint (str): URL endpoint
            params (dict, optional): Endpoint parameters

        Returns:
            list[dict[str, Any]] | dict[str, Any]: Response from API
        """
        return self.generic_request(
            http_method="DELETE", endpoint=endpoint, params=params
        )

    def put(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """HTTP PUT request

        Args:
            endpoint (str): URL endpoint
            ep_params (dict, optional): Endpoint parameters
            json (dict, optional): Data payload

        Returns:
            list[dict[str, Any]] | dict[str, Any]: Response from API
        """
        return self.generic_request(
            http_method="PUT", endpoint=endpoint, params=params, json=json
        )
