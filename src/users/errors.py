from src.core.schemas.base import CustomAPIException


class EmailAlreadyExistsExceptionError(CustomAPIException):
    """Exception raised when email already exists."""

    code = " EMAIL_ALREADY_EXISTS"
    message = "Email already exists..."
    field = "email"
    location = "body"
    status_code = 409
