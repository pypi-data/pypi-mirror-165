"""Classes related to database endpoints
"""

from datetime import datetime
from typing import ClassVar, Optional

from typing_extensions import Self

from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.generic import GenericTemplateWithoutArchive


class Database(GenericTemplateWithoutArchive):
    """Database object class with related methods"""

    BASE_EP: ClassVar[str] = "/database"

    description: Optional[str]
    features: list[str]
    cache_field_values_schedule: str
    timezone: str
    auto_run_queries: bool
    metadata_sync_schedule: str
    caveats: Optional[str]
    is_full_sync: bool
    updated_at: datetime
    native_permissions: Optional[str]
    details: dict
    is_sample: bool
    is_on_demand: bool
    options: Optional[str]
    engine: str
    refingerprint: Optional[str]
    created_at: datetime
    points_of_interest: Optional[str]
    schedules: Optional[dict]

    @classmethod
    def get(
        cls, adapter: MetabaseApi, targets: Optional[list[int]] = None
    ) -> list[Self]:
        """Fetch a list of databases using the provided MetabaseAPI

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int], optional): Database IDs to fetch or returns all

        Returns:
            list[Database]: List of databases requested
        """
        return super(Database, cls).get(adapter=adapter, targets=targets)

    @classmethod
    def create(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Create new databases

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            payloads (list[dict]): Details of database to create

        Returns:
            list[Database]: List of databases created
        """
        return super(Database, cls).create(adapter=adapter, payloads=payloads)

    @classmethod
    def update(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Update existing databases

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            payloads (list[dict]): Details of databases to update

        Returns:
            list[Database]: List of updated databases
        """
        return super(Database, cls).update(adapter=adapter, payloads=payloads)

    @classmethod
    def search(
        cls,
        adapter: MetabaseApi,
        search_params: list[dict],
        search_list: Optional[list] = None,
    ) -> list[Self]:
        """Search for database based on provided criteria

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            search_params (list[dict]): Search criteria; 1 result per
            search_list (list, optional): Search existing list or pulls from API

        Returns:
            list[Database]: List of databases from results
        """
        return super(Database, cls).search(
            adapter=adapter,
            search_params=search_params,
            search_list=search_list,
        )
