import re

from ninja import ModelSchema
import ninja_schema
from ninja.errors import HttpError
from pydantic.functional_validators import field_validator
from django.utils.translation import gettext as _
from config.settings.settings import ABSOLUTE_URL
from src.core.models import Image


class ImageInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for uploading image to server side.
    """
    filename: str
    image: str

    @field_validator('filename')
    @classmethod
    def clean_filename(cls, filename: str) -> str:
        image_types = ['jpeg', 'jpg', 'png',
                       'svg', 'webp', ]
        pattern = r'^[a-zA-Z0-9_-]{1,255}\.[a-zA-Z0-9]+$'
        if re.match(pattern, filename) is None:
            raise HttpError(403,
                            f"Field filename is not valid "
                            f"filename have to correspond "
                            f"to next regular expression "
                            f"{pattern}")
        name, extension = filename.split('.')
        if extension not in image_types:
            raise HttpError(403,
                            _(f'Дозволено відправляти тільки {image_types}'))
        return filename

    class Config:
        model = Image
        include = ['image', 'alt']
        optional = ['alt']


class ImageOutSchema(ModelSchema):
    """
    Pydantic schema for return image to client side.
    """
    image: str
    image_webp: str

    @staticmethod
    def resolve_image(obj: Image):
        return ABSOLUTE_URL + str(obj.image.url)

    @staticmethod
    def resolve_image_webp(obj: Image):
        extension = obj.image.name.split('.')[-1]
        if extension != 'svg':
            return ABSOLUTE_URL + str(obj.image_webp.url)
        else:
            return ABSOLUTE_URL + str(obj.image.url)

    class Meta:
        model = Image
        fields = ['image', 'alt']


class ImageUpdateSchema(ImageInSchema):
    """
    Pydantic schema for updating image.
    """
    filename: str = None

    @field_validator('filename')
    @classmethod
    def clean_filename(cls, filename: str) -> str:
        image_types = ['jpeg', 'jpg', 'png',
                       'svg', 'webp', ]
        pattern = r'^[a-zA-Z0-9_-]{1,255}\.[a-zA-Z0-9]+$'
        if re.match(pattern, filename) is None:
            raise HttpError(403,
                            f"Field filename is not valid "
                            f"filename have to correspond "
                            f"to next regular expression "
                            f"{pattern}")
        name, extension = filename.split('.')
        if extension not in image_types:
            raise HttpError(403,
                            _(f'Дозволено відправляти тільки {image_types}'))
        return filename

    class Config:
        model = Image
        include = ['image', 'alt']
        optional = ['alt', 'image']
