"""Classes related to collections endpoints
"""
from __future__ import annotations  # Included for support of |

from typing import Any, ClassVar, Optional

from metabase_tools.exceptions import EmptyDataReceived
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.generic import GA, GenericWithArchive


class Collection(GenericWithArchive):
    """Collection object class with related methods"""

    BASE_EP: ClassVar[str] = "/collection"

    description: Optional[str]
    archived: Optional[bool]
    slug: Optional[str]
    color: Optional[str]
    personal_owner_id: Optional[int]
    location: Optional[str]
    namespace: Optional[int]
    effective_location: Optional[str]
    effective_ancestors: Optional[list[dict[str, Any]]]
    can_write: Optional[bool]
    parent_id: Optional[int]

    @classmethod
    def get_tree(cls: type[GA], adapter: MetabaseApi) -> list[dict[str, Any]]:
        """Collection tree

        Args:
            adapter (MetabaseApi): Connection to Metabase API

        Raises:
            EmptyDataReceived: No data returned from API

        Returns:
            list[dict]: Representation of collection tree
        """
        response = adapter.get(endpoint="/collection/tree")
        if isinstance(response, list) and all(
            isinstance(record, dict) for record in response
        ):
            return response
        raise EmptyDataReceived

    @staticmethod
    def _flatten_tree(parent: dict[str, Any], path: str = "/") -> list[dict[str, Any]]:
        """Recursive function to flatten collection tree to show the full path for all\
             collections

        Args:
            parent (dict): Parent collection
            path (str, optional): Path to parent collection. Defaults to "/".

        Returns:
            list[dict]: Flattened list
        """
        children = []
        for child in parent["children"]:
            children.append(
                {
                    "id": child["id"],
                    "name": child["name"],
                    "path": f'{path}/{parent["name"]}/{child["name"]}'.replace(
                        "//", "/"
                    ),
                }
            )
            if "children" in child and len(child["children"]) > 0:
                grandchildren = Collection._flatten_tree(
                    child, f'{path}/{parent["name"]}'.replace("//", "/")
                )
                if isinstance(grandchildren, list):
                    children.extend(grandchildren)
                else:
                    children.append(grandchildren)
        return children

    @classmethod
    def get_flat_list(cls, adapter: MetabaseApi) -> list[dict[str, Any]]:
        """Flattens collection tree so the full path of each collection is shown

        Args:
            adapter (MetabaseApi): Connection to Metabase API

        Returns:
            list[dict]: Flattened collection tree
        """
        tree = cls.get_tree(adapter=adapter)
        folders = []
        for root_folder in tree:
            if root_folder["personal_owner_id"] is not None:  # Skips personal folders
                continue
            folders.append(
                {
                    "id": root_folder["id"],
                    "name": root_folder["name"],
                    "path": f'/{root_folder["name"]}',
                }
            )
            folders.extend(Collection._flatten_tree(root_folder))
        return folders

    @classmethod
    def get_contents(
        cls,
        adapter: MetabaseApi,
        collection_id: int,
        model_type: Optional[str] = None,
        archived: bool = False,
    ) -> list[dict[str, Any]]:
        """Get the contents of the provided collection

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            collection_id (int): ID of the requested collection
            model_type (str, optional): Filter to provided model. Defaults to all.
            archived (bool, optional): Archived objects. Defaults to False.

        Raises:
            EmptyDataReceived: No results from API

        Returns:
            list: Contents of collection
        """
        params: dict[Any, Any] = {}
        if archived:
            params["archived"] = archived
        if model_type:
            params["model"] = model_type

        response = adapter.get(
            endpoint=f"/collection/{collection_id}/items",
            params=params,
        )

        if isinstance(response, list) and all(
            isinstance(record, dict) for record in response
        ):
            return response
        raise EmptyDataReceived

    @classmethod
    def graph(cls, adapter: MetabaseApi) -> dict[str, Any]:
        """Graph of collection

        Args:
            adapter (MetabaseApi): Connection to Metabase API

        Returns:
            dict: graph of collection
        """
        result = adapter.get(endpoint="/collection/graph")
        if isinstance(result, dict):
            return result
        raise EmptyDataReceived
