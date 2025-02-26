"""Module with core schemas and enums for project"""

import re

import ninja_schema
from django.utils.translation import gettext as _
from ninja import ModelSchema
from pydantic.functional_validators import field_validator

from config.settings.settings import ABSOLUTE_URL
from src.core.errors import UnprocessableEntityExceptionError
from src.core.models import Gallery
from src.core.models import Image
from src.core.schemas.images import ImageOutSchema


class GalleryInSchema(ninja_schema.ModelSchema):
    """Pydantic schema for uploading image to server side."""

    @ninja_schema.model_validator("images")
    def clean_images(cls, images) -> list:
        Image.objects.check_of_ids(images)
        return images

    class Config:
        model = Gallery
        include = ["images"]


class GalleryMinOutSchema(ModelSchema):
    """Pydantic schema for return image to client side."""

    class Meta:
        model = Gallery
        fields = "__all__"


class GalleryOutSchema(ModelSchema):
    """Pydantic schema for return image to client side."""

    images: list[ImageOutSchema]

    class Meta:
        model = Gallery
        fields = "__all__"


class GalleryItemSchema(ninja_schema.ModelSchema):
    """Pydantic schema for uploading image to server side."""

    delete: bool
    filename: str = None

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

    class Config:
        model = Image
        include = ["id", "image", "alt"]
        optional = ["id", "alt", "image"]


class GalleryItemOutSchema(ModelSchema):
    """Pydantic schema for return gallery images to client side."""

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
        fields = "__all__"
