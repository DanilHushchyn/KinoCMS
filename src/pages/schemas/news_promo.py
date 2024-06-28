from typing import List
import ninja_schema
from pydantic.fields import Field
from src.pages.models import NewsPromo
from ninja import ModelSchema
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import (ImageOutSchema, ImageInSchema,
                                     ImageUpdateSchema)


class NewsPromoInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for creating news and promos to server side.
    """

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

    class Meta:
        model = NewsPromo
        fields = ['name',
                  'date_created',
                  'active',
                  'slug', ]


class NewsPromoCardClientOutSchema(ModelSchema):
    """
    Pydantic schema for showing news and promo card in the client site.
    """
    banner: ImageOutSchema

    class Meta:
        model = NewsPromo
        fields = ['name',
                  'banner',
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


class NewsPromoClientOutSchema(ModelSchema):
    """
    Pydantic schema for showing news and promo full data.
    """
    banner: ImageOutSchema
    seo_image: ImageOutSchema

    class Meta:
        model = NewsPromo
        fields = [
            'name',
            'description',
            'seo_title',
            'seo_description',
            'seo_image',
            'promo',
            'gallery',
            'video_link',
            'active',
            'banner',
            'slug', ]


class NewsPromoUpdateSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for updating news and promo.
    """
    banner: ImageUpdateSchema = None
    seo_image: ImageUpdateSchema = None
    gallery: List[GalleryItemSchema] = None

    class Config:
        model = NewsPromo
        exclude = ['id', 'name', 'description', 'promo',
                   'slug', 'date_created']
        optional = "__all__"
