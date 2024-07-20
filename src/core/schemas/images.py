import binascii
import re
from base64 import b64decode

import ninja_schema
from django.utils.translation import gettext as _
from ninja import ModelSchema
from pydantic.functional_validators import field_validator

from config.settings.settings import ABSOLUTE_URL
from src.core.errors import UnprocessableEntityExceptionError
from src.core.models import Image


class ImageInSchema(ninja_schema.ModelSchema):
    """Pydantic schema for uploading image to server side."""

    filename: str
    image: str

    @field_validator("filename")
    def clean_filename(cls, filename: str) -> str:
        image_types = [
            "jpeg",
            "jpg",
            "png",
            "svg",
            "webp",
        ]
        pattern = r"^[a-zA-Z0-9_-]{1,255}\.[a-zA-Z0-9]+$"
        if re.match(pattern, filename) is None:
            msg = _(
                "Поле filename не підходить, "
                "filename має відповідати "
                "наступному регулярному виразу "
                "{pattern}"
            ).format(pattern=pattern)
            raise UnprocessableEntityExceptionError(msg, field="filename")
        name, extension = filename.split(".")
        if extension not in image_types:
            msg = _("Дозволено відправляти тільки {image_types}").format(
                image_types=image_types
            )
            raise UnprocessableEntityExceptionError(msg, field="filename")

        return filename

    @ninja_schema.model_validator("image")
    def clean_base64(cls, value: str) -> str:
        try:
            b64decode(value, validate=True)
        except binascii.Error:
            msg = _("Невірний формат base64 був відправлений")
            raise UnprocessableEntityExceptionError(msg, field="image")
        return value

    class Config:
        model = Image
        include = ["image", "alt"]
        optional = ["alt"]


class ImageOutSchema(ModelSchema):
    """Pydantic schema for return image to client side."""

    image: str
    image_webp: str

    @staticmethod
    def resolve_image(obj: Image):
        return ABSOLUTE_URL + str(obj.image.url)

    @staticmethod
    def resolve_image_webp(obj: Image):
        extension = obj.image.name.split(".")[-1]
        if extension != "svg":
            return ABSOLUTE_URL + str(obj.image_webp.url)
        else:
            return ABSOLUTE_URL + str(obj.image.url)

    class Meta:
        model = Image
        fields = ["image", "alt"]


class ImageUpdateSchema(ImageInSchema):
    """Pydantic schema for updating image."""

    filename: str = None

    @field_validator("filename")
    @classmethod
    def clean_filename(cls, filename: str) -> str:
        image_types = [
            "jpeg",
            "jpg",
            "png",
            "svg",
            "webp",
        ]
        pattern = r"^[a-zA-Z0-9_-]{1,255}\.[a-zA-Z0-9]+$"
        if re.match(pattern, filename) is None:
            msg = _(
                "Поле filename не підходить, "
                "filename має відповідати "
                "наступному регулярному виразу "
                "{pattern}"
            ).format(pattern=pattern)
            raise UnprocessableEntityExceptionError(msg, field="filename")
        name, extension = filename.split(".")
        if extension not in image_types:
            msg = _("Дозволено відправляти тільки {image_types}").format(
                image_types=image_types
            )
            raise UnprocessableEntityExceptionError(msg, field="filename")
        return filename

    class Config:
        model = Image
        include = ["image", "alt"]
        optional = ["alt", "image"]
