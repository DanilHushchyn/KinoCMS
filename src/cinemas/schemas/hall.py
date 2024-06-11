from typing import List
import ninja_schema
from pydantic.fields import Field

from src.cinemas.models import Hall
from ninja import ModelSchema
from ninja.errors import HttpError
from django.utils.translation import gettext as _
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageOutSchema, ImageInSchema, ImageUpdateSchema
from src.core.utils import validate_capitalized
from src.movies.models import TECHS_CHOICES


class HallInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for creating halls to server side.
    """
    @ninja_schema.model_validator('description_uk', 'description_ru',
                                  'seo_title', 'seo_description')
    def clean_capitalize(cls, value) -> int:
        msg = _('Недійсне значення (не написане великими літерами). '
                'З великих літер повинні починатися ('
                'description, seo_title, seo_description)')
        validate_capitalized(value, msg)
        return value

    banner: ImageInSchema
    seo_image: ImageInSchema
    gallery: List[ImageInSchema] = None

    description_uk: str = Field(max_length=2000)
    description_ru: str = Field(max_length=2000)

    class Config:
        model = Hall
        include = [
            'number',
            'description_uk',
            'description_ru',
            'gallery',
            'banner',
            'tech',
            'seo_title',
            'seo_image',
            'seo_description',
        ]
        optional = ['gallery', ]


class HallCardOutSchema(ModelSchema):
    """
    Pydantic schema for showing hall card.
    """

    class Meta:
        model = Hall
        fields = ['number',
                  'date_created',
                  'id', ]


class HallOutSchema(ModelSchema):
    """
    Pydantic schema for showing hall full data.
    """
    banner: ImageOutSchema
    seo_image: ImageOutSchema
    tech_display: str

    @staticmethod
    def resolve_tech_display(obj: Hall) -> str:
        tech_display = dict(TECHS_CHOICES)[obj.tech]
        return tech_display

    @staticmethod
    def resolve_tech(obj: Hall) -> str:
        return obj.tech

    class Meta:
        model = Hall
        fields = ['number',
                  'description_uk',
                  'description_ru',
                  'gallery',
                  'banner',
                  'id',
                  'tech',
                  'seo_title',
                  'seo_image',
                  'seo_description',
                  ]


class HallUpdateSchema(HallInSchema):
    """
    Pydantic schema for updating hall.
    """
    banner: ImageUpdateSchema = None
    seo_image: ImageUpdateSchema = None
    gallery: List[GalleryItemSchema] = None

    class Config(HallInSchema.Config):
        include = [
            'number',
            'description_uk',
            'description_ru',
            'gallery',
            'banner',
            'seo_title',
            'seo_image',
            'seo_description',
        ]
        optional = '__all__'
