from enum import Enum
from ninja import Schema


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
