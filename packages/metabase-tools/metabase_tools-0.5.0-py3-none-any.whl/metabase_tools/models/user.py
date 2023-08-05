"""Classes related to user endpoints
"""

from datetime import datetime
from typing import ClassVar, Optional

from pydantic.fields import Field
from typing_extensions import Self

from metabase_tools.exceptions import RequestFailure
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.generic import GenericTemplateWithoutArchive


class User(GenericTemplateWithoutArchive):
    """User object class with related methods"""

    BASE_EP: ClassVar[str] = "/user"

    name: str = Field(alias="common_name")
    email: str
    first_name: str
    last_name: str
    date_joined: datetime
    last_login: Optional[datetime]
    updated_at: Optional[datetime]
    is_qbnewb: bool
    is_superuser: bool
    ldap_auth: Optional[bool]
    google_auth: Optional[bool]
    is_active: Optional[bool]
    locale: Optional[str]
    group_ids: Optional[list[int]]
    login_attributes: Optional[list]
    personal_collection_id: Optional[int]

    @classmethod
    def get(
        cls, adapter: MetabaseApi, targets: Optional[list[int]] = None
    ) -> list[Self]:
        """Fetch a list of users using the provided MetabaseAPI

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int], optional): User IDs to fetch or returns all

        Returns:
            list[User]: List of users requested
        """
        return super(User, cls).get(adapter=adapter, targets=targets)

    @classmethod
    def create(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Create new users

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            payloads (list[dict]): Details of users to create

        Returns:
            list[User]: List of users created
        """
        return super(User, cls).create(adapter=adapter, payloads=payloads)

    @classmethod
    def update(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Update existing users

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            payloads (list[dict]): Details of users to update

        Returns:
            list[User]: List of updated users
        """
        return super(User, cls).update(adapter=adapter, payloads=payloads)

    @classmethod
    def search(
        cls,
        adapter: MetabaseApi,
        search_params: list[dict],
        search_list: Optional[list] = None,
    ) -> list[Self]:
        """Search for users based on provided criteria

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            search_params (list[dict]): Search criteria; 1 result per
            search_list (list, optional): Search existing list or pulls from API

        Returns:
            list[User]: List of users from results
        """
        return super(User, cls).search(
            adapter=adapter,
            search_params=search_params,
            search_list=search_list,
        )

    @classmethod
    def current(cls, adapter: MetabaseApi) -> Self:
        """Current user details

        Args:
            adapter (MetabaseApi): Connection to Metabase API

        Raises:
            RequestFailure: Invalid response from API

        Returns:
            User: Current user details
        """
        response = adapter.get(endpoint="/user/current")
        if isinstance(response, dict):
            return cls(**response)
        raise RequestFailure

    @classmethod
    def delete(cls, adapter: MetabaseApi, targets: list[int]) -> dict:
        """Disables user(s) provided

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): List of users to disable

        Returns:
            dict: Dict of users that were disabled with results
        """
        # This method is provided to override the super class' delete function
        return cls.disable(adapter=adapter, targets=targets)

    @classmethod
    def disable(cls, adapter: MetabaseApi, targets: list[int]) -> dict:
        """Disables user(s) provided

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): List of users to disable

        Returns:
            dict: Dict of users that were disabled with results
        """
        return super(User, cls).delete(adapter=adapter, targets=targets)

    @classmethod
    def enable(cls, adapter: MetabaseApi, targets: list[int]) -> list[Self]:
        """Enable user(s) provided

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): List of users to enable

        Returns:
            list[User]: Enabled users
        """
        results = cls._request_list(
            http_method="PUT",
            adapter=adapter,
            endpoint="/user/{id}/reactivate",
            source=[{"id": target} for target in targets],
        )
        return [cls(**result) for result in results]

    @classmethod
    def resend_invite(cls, adapter: MetabaseApi, targets: list[int]) -> list[Self]:
        """Resent user invites

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): List of users to resend invites for

        Returns:
            list[User]: Users with a resent invite
        """
        results = cls._request_list(
            http_method="PUT",
            adapter=adapter,
            endpoint="/user/{id}/send_invite",
            source=[{"id": target} for target in targets],
        )
        return [cls(**result) for result in results]

    @classmethod
    def update_password(cls, adapter: MetabaseApi, payloads: list[dict]) -> list[Self]:
        """Updates passwords for users

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            payloads (list[dict]): List of users and passwords to update

        Returns:
            list[User]: List of users with reset passwords
        """
        results = cls._request_list(
            http_method="PUT",
            adapter=adapter,
            endpoint="/user/{id}/password",
            source=payloads,
        )
        return [cls(**result) for result in results]

    @classmethod
    def qbnewb(cls, adapter: MetabaseApi, targets: list[int]) -> list[Self]:
        """Indicate that a user has been informed about Query Builder.

        Args:
            adapter (MetabaseApi): Connection to Metabase API
            targets (list[int]): List of users to toggle

        Returns:
            list[Self]: Users with query builder toggle set
        """
        results = cls._request_list(
            http_method="PUT",
            adapter=adapter,
            endpoint="/user/{id}/qbnewb",
            source=[{"id": target} for target in targets],
        )
        return [cls(**result) for result in results]
