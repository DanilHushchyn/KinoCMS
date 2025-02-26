"""Exceptions schema."""

from src.core.schemas.base import CustomAPIException


class NotUniqueFieldExceptionError(CustomAPIException):
    """Exception raised when field isn't unique in db."""

    code = "NOT_UNIQUE"
    message = "Field isn't unique."
    field = "field"
    location = "body"
    status_code = 409

    def __init__(
        self, field: str, message: str | None = None, code: str | None = None
    ) -> None:
        self.code = "_".join([field.upper(), self.code])
        super().__init__(message=message, field=field, code=code)


class TicketAlreadyBoughtExceptionError(CustomAPIException):
    """Exception raised when field isn't unique in db."""

    code = "TICKET_ALREADY_BOUGHT"
    message = "..."
    field = ""
    location = "body"
    status_code = 409

    def __init__(
        self,
        field: str | None = None,
        message: str | None = None,
        code: str | None = None,
    ) -> None:
        super().__init__(message=message, field=field, code=code)


class NotFoundExceptionError(CustomAPIException):
    """Exception raised when row wasn't found in db."""

    code = "NOT_FOUND"
    message = "Instance wasn't found."
    field = ""
    location = "db"
    status_code = 404

    def __init__(
        self,
        cls_model: object,
        message: str | None = None,
        field: str | None = None,
        code: str | None = None,
    ) -> None:
        self.code = "_".join([cls_model.__name__.upper(), self.code])
        super().__init__(message=message, field=field, code=code)


class UnprocessableEntityExceptionError(CustomAPIException):
    """Exception raised when validation of schema error."""

    code = "UNPROCESSABLE_ENTITY"
    message = "Details of error."
    field = ""
    location = "body"
    status_code = 422


class AuthenticationExceptionError(CustomAPIException):
    """Exception raised when validation of schema error."""

    code = "AUTHENTICATION_FAILED"
    message = "Details of error."
    field = ""
    location = "body"
    status_code = 401


class InvalidTokenExceptionError(CustomAPIException):
    """Exception raised when validation of schema error."""

    code = "INVALID_TOKEN"
    message = "Details of error."
    field = "API-KEY"
    location = "header"
    status_code = 401


class BodyIsEmptyExceptionError(CustomAPIException):
    """Exception raised when row wasn't found in db."""

    code = "BODY_IS_EMPTY"
    message = "Body is empty."
    field = ""
    location = "body"
    status_code = 422

    def __init__(
        self,
        message: str | None = None,
        field: str | None = None,
        code: str | None = None,
    ) -> None:
        super().__init__(message=message, field=field, code=code)


class SmthWWExceptionError(CustomAPIException):
    """Exception raised when something went wrong."""

    code = "SOMETHING_WENT_WRONG"
    message = "Details of error."
    field = ""
    location = ""
    status_code = 402
