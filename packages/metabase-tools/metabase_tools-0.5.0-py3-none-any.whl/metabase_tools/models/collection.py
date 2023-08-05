"""Classes related to collections endpoints
"""

from typing import ClassVar, Optional

from typing_extensions import Self

from metabase_tools.exceptions import EmptyDataReceived
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.generic import GenericTemplateWithArchive


class Collection(GenericTemplateWithArchive):
    """Collection object class with related methods"""

    BASE_EP: ClassVar[str] = "/collection"

    id: int | str  # root is a valid id for a collection
    description: Optional[str]
    archived: Optional[bool]
    slug: Optional[str]
    color: Optional[str]
    personal_owner_id: Optional[int]
    location: Optional[str]
    namespace: Optional[int]
    effective_location: Optional[str]
    effective_ancestors: Optional[list[dict]]
    can_write: Optional[bool]
    parent_id: Optional[int]

    @classmethod
    def get(
        cls, adapter: MetabaseApi, targets: Optional[list[int]] = None
    ) -> list[Self]:
        """Fetch a list of collections using the provided MetabaseAPI

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int], optional): Collection IDs to fetch or returns all

        Returns:
            list[Collection]: List of collections requested
        """
        return super(Collection, cls).get(adapter=adapter, targets=targets)

    @classmethod
    def create(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Create new collections

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            payloads (list[dict]): Details of collections to create

        Returns:
            list[Collection]: List of collections created
        """
        return super(Collection, cls).create(adapter=adapter, payloads=payloads)

    @classmethod
    def update(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Update existing collections

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            payloads (list[dict]): Details of collections to update

        Returns:
            list[Collection]: List of updated collections
        """
        return super(Collection, cls).update(adapter=adapter, payloads=payloads)

    @classmethod
    def archive(
        cls, adapter: MetabaseApi, targets: list[int], unarchive=False
    ) -> list[Self]:
        """Archive collections

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Collection IDs to archive
            unarchive (bool, optional): Unarchive targets. Defaults to False.

        Returns:
            list[Collection]: List of archived collections
        """
        return super(Collection, cls).archive(
            adapter=adapter,
            targets=targets,
            unarchive=unarchive,
        )

    @classmethod
    def search(
        cls,
        adapter: MetabaseApi,
        search_params: list[dict],
        search_list: Optional[list] = None,
    ) -> list[Self]:
        """Search for collection based on provided criteria

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            search_params (list[dict]): Search criteria; 1 result per
            search_list (list, optional): Search existing list or pulls from API

        Returns:
            list[Collection]: List of collections from results
        """
        return super(Collection, cls).search(
            adapter=adapter,
            search_params=search_params,
            search_list=search_list,
        )

    @classmethod
    def get_tree(cls, adapter: MetabaseApi) -> list[dict]:
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
    def _flatten_tree(parent: dict, path: str = "/") -> list[dict]:
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
    def get_flat_list(cls, adapter: MetabaseApi) -> list[dict]:
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
    ) -> list:
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
        params = {}
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
    def graph(cls, adapter: MetabaseApi) -> dict:
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
