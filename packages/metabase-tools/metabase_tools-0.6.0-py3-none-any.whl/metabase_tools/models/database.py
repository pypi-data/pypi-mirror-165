"""Classes related to database endpoints
"""

from datetime import datetime
from typing import Any, ClassVar, Optional

from metabase_tools.models.generic import GenericWithoutArchive


class Database(GenericWithoutArchive):
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
    details: dict[str, Any]
    is_sample: bool
    is_on_demand: bool
    options: Optional[str]
    engine: str
    refingerprint: Optional[str]
    created_at: datetime
    points_of_interest: Optional[str]
    schedules: Optional[dict[str, Any]]
