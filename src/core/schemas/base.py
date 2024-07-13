from enum import Enum
from ninja import Schema
from ninja_extra.exceptions import APIException


class MessageOutSchema(Schema):
    """
    Pydantic schema for return message to client side.

    Purpose of this schema just say that operation
    has been successful or failed
    """

    detail: str | None


class LangEnum(Enum):
    Ukrainian = "uk"
    Russian = "ru"

    @classmethod
    def _missing_(cls, value):
        return cls.Ukrainian


class DirectionEnum(Enum):
    Ascending = "ascending"
    Descending = "descending"

    @classmethod
    def _missing_(cls, value):
        return cls.Descending


class DetailErrorFieldsSchema(Schema):
    """Error detail fields schema."""

    location: str = ""
    field: str = ""
    message: str = ""


class DetailErrorSchema(Schema):
    """Detail category error schema."""

    code: str
    details: list[DetailErrorFieldsSchema]


class ErrorSchema(Schema):
    """Error schema about category bot found."""

    status: int = 000
    error: DetailErrorSchema


class CustomAPIException(APIException):
    """Category exception."""

    status_code: int
    code: str
    message: str
    field: str
    location: str

    def __init__(self, message: str | None = None,
                 field: str | None = None,
                 code: str | None = None) -> None:
        """Initialize exception."""
        if message is not None:
            self.message = message
        if field is not None:
            self.field = field
        if code is not None:
            self.code = code

        error_detail = DetailErrorSchema(
            code=self.code,
            details=[
                DetailErrorFieldsSchema(
                    location=self.location,
                    field=self.field,
                    message=self.message,
                )
            ],
        )
        error = ErrorSchema(
            status=self.status_code,
            error=error_detail,
        )
        self.status_code = self.status_code
        self.detail = error.dict()
        self.error_detail = error_detail.dict()

    def __dict__(self):
        return {
            'summary': self.code,
            'value': {
                "status": self.status_code,
                "error": self.error_detail
            }
        }


def errors_to_docs(responses: dict) -> dict:
    result = {}
    for status, errors in responses.items():
        result[status] = {
            "content": {
                "application/json": {
                    "examples": {
                    }
                }
            },
        }
        for key, error in enumerate(errors):
            result[status]["content"]["application/json"]["examples"][key] = \
                {
                    "summary": error.code,
                    "description": f"{error.code}",
                    "value": error.detail
                }
    return result
