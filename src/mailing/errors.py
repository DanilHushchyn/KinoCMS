"""All custom possible error along mailing process"""

from src.core.schemas.base import CustomAPIException


class MailingIsActiveExceptionError(CustomAPIException):
    """Exception raised when mailing is active."""

    code = "MAILING_IS_ACTIVE"
    message = "Mailing is active..."
    field = ""
    location = ""
    status_code = 400


class MailingIsNotActiveExceptionError(CustomAPIException):
    """Exception raised when mailing is active."""

    code = "MAILING_IS_NOT_ACTIVE"
    message = "Mailing is not active..."
    field = ""
    location = ""
    status_code = 400
