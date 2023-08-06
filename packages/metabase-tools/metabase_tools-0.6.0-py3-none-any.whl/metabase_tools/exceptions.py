"""Exceptions for the MetabaseApi class
"""


class MetabaseApiException(Exception):
    """Base exception for other exceptions included in this package"""


class AuthenticationFailure(MetabaseApiException):
    """Error encountered while trying to authenticate with API"""


class EmptyDataReceived(MetabaseApiException):
    """Response received but it contained no data"""


class InvalidDataReceived(MetabaseApiException):
    """Data received but it could not be decoded"""


class InvalidParameters(MetabaseApiException):
    """Invalid parameters supplied to API"""


class ItemNotFound(MetabaseApiException):
    """Item was not found it the listed location"""


class ItemInPersonalCollection(MetabaseApiException):
    """Requested item is in a personal collection"""


class RequestFailure(MetabaseApiException):
    """HTTP error encountered during request"""


class NoUpdateProvided(MetabaseApiException):
    """An update was requested but no change was provided"""
