from typing import List, Any
import ninja_schema
from pydantic.fields import Field
from src.pages.models import NewsPromo
from ninja import ModelSchema
from ninja.errors import HttpError
from django.utils.translation import gettext as _
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageOutSchema, ImageInSchema, ImageUpdateSchema
from src.core.utils import validate_capitalized, validate_max_length
from pydantic import BaseModel, Json, ValidationError


class NewsPromoInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for creating news and promos to server side.
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
    seo_image: ImageInSchema
    gallery: List[ImageInSchema] = None
    name_uk: str = Field(max_length=100)
    name_ru: str = Field(max_length=100)
    description_uk: str = Field(max_length=2000)
    description_ru: str = Field(max_length=2000)

    class Config:
        model = NewsPromo
        exclude = ['id', 'name', 'description',
                   'slug', 'date_created']
        optional = ['gallery', ]


class NewsPromoCardOutSchema(ModelSchema):
    """
    Pydantic schema for showing news and promo card.
    """
    banner: ImageOutSchema

    class Meta:
        model = NewsPromo
        fields = ['name',
                  'date_created',
                  'slug', ]


class NewsPromoOutSchema(ModelSchema):
    """
    Pydantic schema for showing news and promo full data.
    """
    banner: ImageOutSchema
    seo_image: ImageOutSchema

    class Meta:
        model = NewsPromo
        exclude = ['id', 'name', 'description',
                   'slug', 'date_created']


class NewsPromoUpdateSchema(NewsPromoInSchema):
    """
    Pydantic schema for updating news and promo.
    """
    banner: ImageUpdateSchema = None
    seo_image: ImageUpdateSchema = None
    gallery: List[GalleryItemSchema] = None

    class Config:
        model = NewsPromo
        exclude = ['id', 'name', 'description',
                   'slug', 'date_created']
        optional = "__all__"
