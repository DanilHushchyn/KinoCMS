from enum import Enum
from ninja import Field, ModelSchema, Schema


class MessageOutSchema(Schema):
    """
    Pydantic schema for return message to client side.

    Purpose of this schema just say that operation
    has been successful or failed
    """

    message: str | None


class LangEnum(Enum):
    Ukrainian = "uk"
    Russian = "ru"
