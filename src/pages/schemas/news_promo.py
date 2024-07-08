from typing import List
import ninja_schema
from pydantic.fields import Field
from src.core.errors import (UnprocessableEntityExceptionError,
                             NotFoundExceptionError)
from src.pages.models import NewsPromo, Tag
from ninja import ModelSchema
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import (ImageOutSchema, ImageInSchema,
                                     ImageUpdateSchema)
from django.utils.translation import gettext as _


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

    @ninja_schema.model_validator('tags')
    def clean_tags(cls, tag_ids: List[int]) -> List[int]:
        if len(tag_ids) > 5:
            msg = _('Максимальна кількість тегів 5')
            raise UnprocessableEntityExceptionError(message=msg)
        tags_db = list(Tag.objects
                       .filter(id__in=tag_ids)
                       .values_list('id', flat=True))
        if len(tag_ids) != len(tags_db):
            diff = list(set(tag_ids) ^ set(tags_db))
            msg = (_('У заданому переліку тегів є '
                     'ids {diff} які не присутні у базі')
                   .format(diff=diff))
            raise NotFoundExceptionError(message=msg,
                                         cls_model=Tag,
                                         field='tags')
        return tag_ids

    class Config:
        model = NewsPromo
        exclude = ['id', 'name', 'description',
                   'slug', 'date_created']
        optional = ['gallery', ]


class TagOutSchema(ModelSchema):
    """
    Pydantic schema for showing tag info.
    """

    class Meta:
        model = Tag
        fields = ['name',
                  'color',
                  'id']


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
    tags: List[TagOutSchema]

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
    tags: List[TagOutSchema]

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

    @ninja_schema.model_validator('tags')
    def clean_tags(cls, tag_ids: List[int]) -> List[int]:
        if len(tag_ids) > 5:
            msg = _('Максимальна кількість тегів 5')
            raise UnprocessableEntityExceptionError(message=msg)
        tags_db = list(Tag.objects
                       .filter(id__in=tag_ids)
                       .values_list('id', flat=True))
        if len(tag_ids) != len(tags_db):
            diff = list(set(tag_ids) ^ set(tags_db))
            msg = (_('У заданому переліку тегів є '
                     'ids {diff} які не присутні у базі')
                   .format(diff=diff))
            raise NotFoundExceptionError(message=msg,
                                         cls_model=Tag,
                                         field='tags')
        return tag_ids

    class Config:
        model = NewsPromo
        exclude = ['id', 'name', 'description', 'promo',
                   'slug', 'date_created']
        optional = "__all__"
