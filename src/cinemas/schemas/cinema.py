from typing import List, Any
import ninja_schema
from ninja_extra.schemas.response import PaginatedResponseSchema
from pydantic.fields import Field

from config.settings.settings import GOOGLE_MAPS_API_KEY
from src.cinemas.models import Cinema
from ninja import ModelSchema
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import (ImageOutSchema, ImageInSchema,
                                     ImageUpdateSchema)
from pydantic import Json
from src.core.utils import check_phone_number
from src.movies.models import Tech
from src.movies.schemas import TechOutSchema


class CinemaInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for creating cinemas to server side.
    """

    @ninja_schema.model_validator('phone_1')
    def validate_phone_1(cls, value) -> str:
        check_phone_number(value)
        return value

    @ninja_schema.model_validator('phone_2')
    def validate_phone_2(cls, value) -> str:
        check_phone_number(value)
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

    @staticmethod
    def resolve_phone_1(obj: Cinema):
        return str(obj.phone_1)

    @staticmethod
    def resolve_phone_2(obj: Cinema):
        return str(obj.phone_2)

    class Meta:
        model = Cinema
        exclude = ['id', 'name', 'description', 'address',
                   'terms', 'slug', 'date_created']


class CinemaClientOutSchema(ModelSchema):
    """
    Pydantic schema for showing cinema full data in client site.
    """
    banner: ImageOutSchema
    logo: ImageOutSchema
    seo_image: ImageOutSchema
    techs: List[TechOutSchema]

    @staticmethod
    def resolve_techs(obj: Cinema) -> List[Tech]:
        obj.hall_set.select_related('tech').all()
        techs = []
        for hall in obj.hall_set.select_related('tech').all():
            techs.append(hall.tech)
        techs = list(set(techs))
        return techs

    @staticmethod
    def resolve_phone_1(obj: Cinema):
        return str(obj.phone_1)

    @staticmethod
    def resolve_phone_2(obj: Cinema):
        return str(obj.phone_2)

    class Meta:
        model = Cinema
        fields = ['name',
                  'description',
                  'gallery',
                  'terms',
                  'slug',
                  ]


class CinemaContactOutSchema(ModelSchema):
    """
    Pydantic schema for showing cinema contacts.
    """
    banner: ImageOutSchema
    logo: ImageOutSchema

    @staticmethod
    def resolve_phone_1(obj: Cinema):
        return str(obj.phone_1)

    @staticmethod
    def resolve_phone_2(obj: Cinema):
        return str(obj.phone_2)

    class Meta:
        model = Cinema
        fields = ['slug', 'name', 'address',
                  'email', 'banner', 'logo',
                  'phone_1', 'phone_2',
                  'coordinate']


class PaginatedContactsResponseSchema(PaginatedResponseSchema):
    """
    Pydantic schema for paginating cinema contacts.
    """
    google_maps_api_key: str = GOOGLE_MAPS_API_KEY


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
