"""Exceptions schema."""

from src.core.schemas.base import CustomAPIException


class NotUniqueFieldExceptionError(CustomAPIException):
    """Exception raised when field isn't unique in db."""

    code = "NOT_UNIQUE"
    message = "Field isn't unique."
    field = "field"
    location = "body"
    status_code = 409


class NotFoundExceptionError(CustomAPIException):
    """Exception raised when row wasn't found in db."""

    code = "NOT_FOUND"
    message = "Instance wasn't found."
    field = ""
    location = ""
    status_code = 404


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
