"""Unofficial API wrapper for Metabase
"""

__version__ = "0.6.0"

from metabase_tools.exceptions import (
    AuthenticationFailure,
    EmptyDataReceived,
    InvalidDataReceived,
    InvalidParameters,
    ItemInPersonalCollection,
    ItemNotFound,
    MetabaseApiException,
    NoUpdateProvided,
    RequestFailure,
)
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.card import Card
from metabase_tools.models.collection import Collection
from metabase_tools.models.database import Database
from metabase_tools.models.user import User
from metabase_tools.tools import MetabaseTools

__all__ = (
    "AuthenticationFailure",
    "EmptyDataReceived",
    "InvalidDataReceived",
    "InvalidParameters",
    "ItemNotFound",
    "ItemInPersonalCollection",
    "MetabaseApiException",
    "NoUpdateProvided",
    "RequestFailure",
    "MetabaseApi",
    "Card",
    "Collection",
    "Database",
    "User",
    "MetabaseTools",
)
