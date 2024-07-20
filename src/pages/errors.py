"""Errors that can be along working with pages"""

from src.core.schemas.base import CustomAPIException


class TooMuchElementsExceptionError(CustomAPIException):
    """Exception raised when elements to much in db."""

    code = "TOO_MUCH_ELEMENTS"
    message = "Too much elements"
    field = ""
    location = ""
    status_code = 409


class PageUnableToDeleteExceptionError(CustomAPIException):
    """Exception raised when page is blocked for deletion."""

    code = "PAGE_UNABLE_TO_DELETE"
    message = "Page unable to delete"
    field = ""
    location = ""
    status_code = 406
