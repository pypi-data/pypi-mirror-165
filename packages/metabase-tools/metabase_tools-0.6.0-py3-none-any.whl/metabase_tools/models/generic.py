"""
    Generic classes for Metabase
"""
from __future__ import annotations  # Included for support of |

from typing import Any, ClassVar, Optional, TypeVar

from pydantic import BaseModel

from metabase_tools.exceptions import EmptyDataReceived, InvalidParameters
from metabase_tools.metabase import MetabaseApi


class MetabaseGenericObject(BaseModel, extra="forbid"):
    """Base class for all Metabase objects. Provides generic fields and methods."""

    BASE_EP: ClassVar[str]

    id: int | str
    name: str

    @classmethod
    def _request_list(
        cls,
        http_method: str,
        adapter: MetabaseApi,
        endpoint: str,
        source: list[int] | list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Sends requests to API based on a list of objects

        Args:
            http_method (str): GET or POST or PUT or DELETE
            adapter (MetabaseApi): Connection to Metabase API
            endpoint (str): Endpoint to use for request
            source (list[int] | list[dict]): List of targets or payloads

        Raises:
            InvalidParameters: Item in source is not an int or dict
            EmptyDataReceived: No data returned

        Returns:
            list[dict]: Aggregated results of all API calls
        """
        results = []

        for item in source:
            if isinstance(item, int):
                response = adapter.generic_request(
                    http_method=http_method, endpoint=endpoint.format(id=item)
                )
            elif isinstance(item, dict):
                item_ep = endpoint.format(**item)
                if http_method == "PUT":
                    response = adapter.put(
                        endpoint=item_ep,
                        json=item,
                    )
                else:
                    response = adapter.generic_request(
                        http_method=http_method,
                        endpoint=item_ep,
                        json=item,
                    )
            else:
                raise InvalidParameters
            if isinstance(response, dict):
                results.append(response)
            elif isinstance(response, list):
                results.extend(response)
        if len(results) > 0:
            return results
        raise EmptyDataReceived("No data returned")


class GenericWithoutArchive(MetabaseGenericObject):
    """Generic class for objects without support for archive"""

    @classmethod
    def get(
        cls: type[GWA], adapter: MetabaseApi, targets: Optional[list[int]] = None
    ) -> list[GWA]:
        """Generic method for returning an object or list of objects

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int], optional): IDs of the objects being requested

        Raises:
            InvalidParameters: Targets are not None or list[int]
            EmptyDataReceived: No data is received from the API

        Returns:
            list[Self]: List of objects of the relevant type
        """
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            results = cls._request_list(
                http_method="GET",
                adapter=adapter,
                endpoint=cls.BASE_EP + "/{id}",
                source=targets,
            )
            return [cls(**result) for result in results]

        if targets is None:
            # If no targets are provided, all objects of that type should be returned
            response = adapter.get(endpoint=cls.BASE_EP)
            if isinstance(response, list):  # Validate data was returned
                # Unpack data into instances of the class and return
                return [
                    cls(**record) for record in response if isinstance(record, dict)
                ]
        else:
            # If something other than None, int or list[int], raise error
            raise InvalidParameters("Invalid target(s)")
        # If response.data was empty, raise error
        raise EmptyDataReceived("No data returned")

    @classmethod
    def search(
        cls: type[GWA],
        adapter: MetabaseApi,
        search_params: list[dict[str, Any]],
        search_list: Optional[list[GWA]] = None,
    ) -> list[GWA]:
        """Method to search a list of objects meeting a list of parameters

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            search_params (list[dict]): Each dict contains search criteria and returns\
                 1 result
            search_list (list[Self], optional): Provide to search against an existing \
                list, by default pulls from API

        Returns:
            list[Self]: List of objects of the relevant type
        """
        objs = search_list or cls.get(adapter=adapter)
        results = []
        for param in search_params:
            for obj in objs:
                obj_dict = obj.dict()
                for key, value in param.items():
                    if key in obj_dict and value == obj_dict[key]:
                        results.append(obj)
        return results

    @classmethod
    def create(
        cls: type[GWA], adapter: MetabaseApi, payloads: list[dict[str, Any]]
    ) -> list[GWA]:
        """Generic method for creating a list of objects

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            payloads (list[dict]): List of json payloads

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            list[Self]: List of objects of the relevant type
        """
        if isinstance(payloads, list) and all(isinstance(t, dict) for t in payloads):
            # If a list of targets is provided, return a list of objects
            results = cls._request_list(
                http_method="POST",
                adapter=adapter,
                endpoint=cls.BASE_EP,
                source=payloads,
            )
            return [cls(**result) for result in results]
        # If something other than dict or list[dict], raise error
        raise InvalidParameters("Invalid target(s)")

    @classmethod
    def update(
        cls: type[GWA], adapter: MetabaseApi, payloads: list[dict[str, Any]]
    ) -> list[GWA]:
        """Generic method for updating a list of objects

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            payloads (list[dict]): List of json payloads

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            list[Self]: List of objects of the relevant type
        """
        if isinstance(payloads, list) and all(isinstance(t, dict) for t in payloads):
            # If a list of targets is provided, return a list of objects
            results = cls._request_list(
                http_method="PUT",
                adapter=adapter,
                endpoint=cls.BASE_EP + "/{id}",
                source=payloads,
            )
            return [cls(**result) for result in results]
        # If something other than dict or list[dict], raise error
        raise InvalidParameters("Invalid target(s)")

    @classmethod
    def delete(cls, adapter: MetabaseApi, targets: list[int]) -> dict[int, Any]:
        """Method to delete a list of objects

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): List of objects to delete

        Raises:
            InvalidParameters: Targets is not a list of ints

        Returns:
            dict: _description_
        """
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            results = cls._request_list(
                http_method="DELETE",
                adapter=adapter,
                endpoint=cls.BASE_EP + "/{id}",
                source=targets,
            )
            return {target: result for result, target in zip(results, targets)}
        raise InvalidParameters("Invalid set of targets")


class GenericWithArchive(GenericWithoutArchive):
    """Generic class for objects with archive support in the API"""

    @classmethod
    def archive(
        cls: type[GA],
        adapter: MetabaseApi,
        targets: list[int],
        unarchive: bool = False,
    ) -> list[GA]:
        """Generic method for archiving a list of objects

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): List of objects to archive
            unarchive (bool): Whether object should be unarchived instead of archived

        Raises:
            InvalidParameters: Targets and jsons are both None

        Returns:
            list[Self]: List of objects of the relevant type
        """
        if isinstance(targets, list) and all(isinstance(t, int) for t in targets):
            results = cls._request_list(
                http_method="PUT",
                adapter=adapter,
                endpoint=cls.BASE_EP + "/{id}",
                source=[
                    {"id": target, "archived": not unarchive} for target in targets
                ],
            )
            return [cls(**result) for result in results]
        raise InvalidParameters("Invalid set of targets")


MGO = TypeVar("MGO", bound="MetabaseGenericObject")
GWA = TypeVar("GWA", bound="GenericWithoutArchive")
GA = TypeVar("GA", bound="GenericWithArchive")
