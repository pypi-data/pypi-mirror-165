"""Classes related to card endpoints
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar, Optional
from uuid import UUID

from pydantic.fields import Field

from metabase_tools.exceptions import (
    EmptyDataReceived,
    InvalidDataReceived,
    RequestFailure,
)
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.collection import Collection
from metabase_tools.models.generic import GA, GenericWithArchive
from metabase_tools.models.user import User


class Card(GenericWithArchive):
    """Card object class with related methods"""

    BASE_EP: ClassVar[str] = "/card"

    description: Optional[str]
    archived: bool
    collection_position: Optional[int]
    table_id: Optional[int]
    result_metadata: Optional[list[dict[str, Any]]]
    creator: User
    database_id: Optional[int]
    enable_embedding: bool
    collection_id: Optional[int]
    query_type: Optional[str]
    creator_id: int
    updated_at: datetime
    made_public_by_id: Optional[int]
    embedding_params: Optional[dict[str, Any]]
    cache_ttl: Optional[str]
    dataset_query: dict[str, Any]
    display: str
    last_edit_info: Optional[dict[str, Any]] = Field(alias="last-edit-info")
    visualization_settings: dict[str, Any]
    collection: Optional[Collection]
    dataset: Optional[int]
    created_at: datetime
    public_uuid: Optional[UUID]
    can_write: Optional[bool]
    dashboard_count: Optional[int]
    is_favorite: Optional[bool] = Field(alias="favorite")

    @classmethod
    def related(
        cls: type[GA], adapter: MetabaseApi, targets: list[int]
    ) -> list[dict[str, Any]]:
        """Objects related to targets

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Card IDs to pull

        Returns:
            list[dict]: List of dicts with related objects for each target
        """
        results = []
        for target in targets:
            new = {"card_id": target}
            result = adapter.get(endpoint=f"/card/{target}/related")
            if isinstance(result, dict):
                new |= result
            results.append(new)
        return results

    @classmethod
    def embeddable(cls: type[GA], adapter: MetabaseApi) -> list[GA]:
        """Fetch list of cards with embedding enabled

        Args:
            adapter (MetabaseApi): Connection to Metabase API

        Raises:
            EmptyDataReceived: If no cards have embedding enabled

        Returns:
            list[Self]: List of cards with embedding enabled
        """
        cards = adapter.get(endpoint="/card/embeddable")
        if cards:
            return [cls(**card) for card in cards if isinstance(card, dict)]
        raise EmptyDataReceived

    @classmethod
    def favorite(
        cls: type[GA], adapter: MetabaseApi, targets: list[int]
    ) -> list[dict[str, Any]]:
        """Favorite cards

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Card IDs to favorite

        Returns:
            list[dict]: Results of favoriting operation
        """
        results = []
        for target in targets:
            try:
                result = adapter.post(endpoint=f"/card/{target}/favorite")
            except RequestFailure:
                result = {
                    "card_id": target,
                    "error": "Metabase error, probably already a favorite",
                }
            if isinstance(result, dict):
                results.append(result)
        return results

    @classmethod
    def unfavorite(
        cls: type[GA], adapter: MetabaseApi, targets: list[int]
    ) -> list[dict[str, Any]]:
        """Unfavorite cards

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Card IDs to unfavorite

        Returns:
            list[dict]: Results of unfavoriting operation
        """
        results = []
        for target in targets:
            result: dict[str, int | bool | str] = {}
            try:
                _ = adapter.delete(endpoint=f"/card/{target}/favorite")
                result = {"card_id": target, "success": True}
            except (InvalidDataReceived, RequestFailure):
                result = {
                    "card_id": target,
                    "error": "Metabase error, probably not a favorite",
                }
            results.append(result)
        return results

    @classmethod
    def share(
        cls: type[GA], adapter: MetabaseApi, targets: list[int]
    ) -> list[dict[str, Any]]:
        """Generate publicly-accessible links for cards

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Card IDs to share

        Returns:
            list[dict]: UUIDs to be used in public links.
        """
        return cls._request_list(
            http_method="POST",
            adapter=adapter,
            endpoint="/card/{id}/public_link",
            source=targets,
        )

    @classmethod
    def unshare(
        cls: type[GA], adapter: MetabaseApi, targets: list[int]
    ) -> list[dict[str, Any]]:
        """Remove publicly-accessible links for cards

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): Card IDs to unshare

        Returns:
            list[dict]: Result of unshare operation
        """
        return cls._request_list(
            http_method="DELETE",
            adapter=adapter,
            endpoint="/card/{id}/public_link",
            source=targets,
        )
