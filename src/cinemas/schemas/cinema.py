from typing import List, Any

import ninja_schema
from django.db.models import Q
from pydantic.fields import Field

from src.cinemas.models import Cinema
from ninja import ModelSchema
from ninja.errors import HttpError
from django.utils.translation import gettext as _
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageOutSchema, ImageInSchema, ImageUpdateSchema
from src.core.utils import validate_capitalized, validate_max_length
from pydantic import BaseModel, Json, ValidationError


class CinemaInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for creating cinemas to server side.
    """

    @ninja_schema.model_validator('name_uk', 'name_ru',
                                  'description_uk', 'description_ru',
                                  'seo_title', 'seo_description')
    def clean_capitalize(cls, value) -> int:
        msg = _('Недійсне значення (не написане великими літерами). '
                'З великих літер повинні починатися (name, '
                'description, seo_title, seo_description)')
        validate_capitalized(value, msg)
        return value

    banner: ImageInSchema
    logo: ImageInSchema
    seo_image: ImageInSchema
    gallery: List[ImageInSchema] = None
    name_uk: str = Field(max_length=100)
    name_ru: str = Field(max_length=100)
    address_uk: str = Field(max_length=2000)
    address_ru: str = Field(max_length=2000)
    description_uk: str = Field(max_length=2000)
    description_ru: str = Field(max_length=2000)
    terms_uk: Json[Any]
    terms_ru: Json[Any]

    class Config:
        model = Cinema
        exclude = ['id', 'name', 'description', 'address',
                   'terms', 'slug', 'date_created']
        optional = ['gallery', ]


class CinemaCardOutSchema(ModelSchema):
    """
    Pydantic schema for showing cinema card.
    """
    banner: ImageOutSchema

    class Meta:
        model = Cinema
        fields = ['name',
                  'banner',
                  'slug', ]


class CinemaOutSchema(ModelSchema):
    """
    Pydantic schema for showing cinema full data.
    """
    banner: ImageOutSchema
    logo: ImageOutSchema
    seo_image: ImageOutSchema

    class Meta:
        model = Cinema
        exclude = ['id', 'name', 'description', 'address',
                   'terms', 'slug', 'date_created']


class CinemaUpdateSchema(CinemaInSchema):
    """
    Pydantic schema for updating cinema.
    """
    banner: ImageUpdateSchema = None
    logo: ImageUpdateSchema = None
    seo_image: ImageUpdateSchema = None
    gallery: List[GalleryItemSchema] = None

    class Config:
        model = Cinema
        exclude = ['id', 'name', 'description', 'address',
                   'terms', 'slug', 'date_created']
        optional = "__all__"
