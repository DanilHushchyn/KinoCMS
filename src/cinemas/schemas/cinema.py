from typing import List, Any
import ninja_schema
from ninja.errors import HttpError
from phonenumber_field.validators import validate_international_phonenumber
from pydantic.fields import Field
from src.cinemas.models import Cinema
from ninja import ModelSchema
from django.utils.translation import gettext as _
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageOutSchema, ImageInSchema, ImageUpdateSchema
from src.core.utils import validate_capitalized
from pydantic import Json
from django.core.exceptions import ValidationError


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

    @ninja_schema.model_validator('phone_1', 'phone_2')
    def clean_phone_number(cls, value) -> str:
        try:
            validate_international_phonenumber(value)
        except ValidationError:
            raise HttpError(403, _("Введено некоректний номер телефону."))
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
