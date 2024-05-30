from typing import List

import ninja_schema
from django.db.models import Q


from src.cinemas.models import Cinema
from ninja import ModelSchema
from ninja.errors import HttpError
from django.utils.translation import gettext as _

from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageOutSchema, ImageInSchema, ImageUpdateSchema
from src.core.utils import validate_capitalized


class CinemaInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for creating cinemas to server side.
    """

    @ninja_schema.model_validator('name_uk', 'name_ru')
    def clean_name(cls, value) -> int:
        if Cinema.objects.filter(Q(name_uk=value) | Q(name_ru=value)).exists():
            msg = _('Поле name повинно бути унікальним. Ця назва вже зайнята')
            raise HttpError(409, msg)
        return value

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

    class Config:
        model = Cinema
        include = [
            'name_uk',
            'name_ru',
            'description_uk',
            'description_ru',
            'logo',
            'gallery',
            'banner',
            'address',
            'coordinate',
            'seo_title',
            'seo_image',
            'seo_description',
        ]
        optional = ['gallery', ]


class CinemaCardOutSchema(ModelSchema):
    """
    Pydantic schema for showing cinema card.
    """
    banner: ImageOutSchema
    logo: ImageOutSchema
    seo_image: ImageOutSchema

    class Meta:
        model = Cinema
        fields = ['name_uk',
                  'name_ru',
                  'description_uk',
                  'description_ru',
                  'logo',
                  'gallery',
                  'banner',
                  'slug',
                  'address',
                  'coordinate',
                  'seo_title',
                  'seo_image',
                  'seo_description',
                  ]


class CinemaUpdateSchema(CinemaInSchema):
    """
    Pydantic schema for updating cinema.
    """
    banner: ImageUpdateSchema = None
    logo: ImageUpdateSchema = None
    seo_image: ImageUpdateSchema = None
    gallery: List[GalleryItemSchema] = None

    class Config(CinemaInSchema.Config):
        include = [
            'name_uk',
            'name_ru',
            'description_uk',
            'description_ru',
            'logo',
            'gallery',
            'banner',
            'address',
            'coordinate',
            'seo_title',
            'seo_image',
            'seo_description',
        ]
        optional = '__all__'
