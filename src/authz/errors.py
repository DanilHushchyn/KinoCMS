from src.core.schemas.base import CustomAPIException


class EmailAlreadyExistsExceptionError(CustomAPIException):
    """Exception raised when field isn't unique in db."""

    code = "EMAIL_ALREADY_EXISTS"
    message = "Email already exists."
    field = "email"
    location = "body"
    status_code = 409

