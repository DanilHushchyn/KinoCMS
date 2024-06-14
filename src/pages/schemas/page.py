from typing import List
import ninja_schema
from pydantic.fields import Field
from src.pages.models import Page
from ninja import ModelSchema
from django.utils.translation import gettext as _
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageOutSchema, ImageInSchema, ImageUpdateSchema
from src.core.utils import validate_capitalized
from typing import List, Any
from pydantic import Json


class PageInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for creating pages to server side.
    """

    @ninja_schema.model_validator('name_uk', 'name_ru',
                                  'seo_title', 'seo_description')
    def clean_capitalize(cls, value) -> int:
        msg = _('Недійсне значення (не написане великими літерами). '
                'З великих літер повинні починатися '
                '(name, seo_title, seo_description)')
        validate_capitalized(value, msg)
        return value

    banner: ImageInSchema
    seo_image: ImageInSchema
    gallery: List[ImageInSchema] = None
    name_uk: str = Field(max_length=100)
    name_ru: str = Field(max_length=100)
    content_uk: Json[Any]
    content_ru: Json[Any]

    class Config:
        model = Page
        exclude = ['id', 'name', 'content', 'can_delete',
                   'slug', 'date_created']
        optional = ['gallery', ]


class PageCardOutSchema(ModelSchema):
    """
    Pydantic schema for showing pages card.
    """

    class Meta:
        model = Page
        fields = ['name',
                  'date_created',
                  'active',
                  'can_delete',
                  'slug', ]


class PageOutSchema(ModelSchema):
    """
    Pydantic schema for showing pages full data.
    """
    banner: ImageOutSchema
    seo_image: ImageOutSchema

    class Meta:
        model = Page
        exclude = ['id', 'name', 'content',
                   'slug', 'date_created']


class PageUpdateSchema(PageInSchema):
    """
    Pydantic schema for updating pages.
    """
    banner: ImageUpdateSchema = None
    seo_image: ImageUpdateSchema = None
    gallery: List[GalleryItemSchema] = None

    class Config:
        model = Page
        exclude = ['id', 'name', 'can_delete', 'content',
                   'slug', 'date_created']
        optional = "__all__"
