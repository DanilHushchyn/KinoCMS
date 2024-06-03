import enum
from enum import Enum
from typing import List, Set, Tuple, Any, Literal

import ninja_schema
from ninja.errors import HttpError
from pydantic.functional_validators import field_validator

from src.movies.models import Movie
from ninja import ModelSchema
from django.utils.translation import gettext as _

from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageOutSchema, ImageInSchema, ImageUpdateSchema
from src.core.utils import validate_capitalized
from django_countries.data import COUNTRIES

from src.users.schemas import UserFieldsEnum

GenresEnum = Enum(
    "GenresEnum",
    ((value, key) for key, value in Movie.GENRES_CHOICES),
    type=str,
)
CountryEnum = Enum(
    "CountryEnum",
    [(str(value), str(key)) for key, value in list(COUNTRIES.items())],
    type=str,
)


class MovieInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for creating Movies to server side.
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

    card_img: ImageInSchema
    seo_image: ImageInSchema
    gallery: List[ImageInSchema] = None
    countries: List[CountryEnum]
    genres: List[GenresEnum]

    @ninja_schema.model_validator('genres')
    def clean_genres(cls, genres) -> List[str]:
        genres = set(genres)
        result = []
        keys = [str(key) for key, value in Movie.GENRES_CHOICES]
        for genre in genres:
            if genre not in keys:
                msg = _(f'List should contain any of '
                        f'{keys}')
                raise HttpError(422, msg)
            result.append(genre.value)
        return result

    @ninja_schema.model_validator('countries')
    def clean_countries(cls, countries) -> List[str]:
        countries = set(countries)
        result = []
        for country in countries:
            if country not in COUNTRIES.keys():
                msg = _(f'List should contain any of '
                        f'{list(COUNTRIES.keys())}')
                raise HttpError(422, msg)
            result.append(country.value)
        return result

    class Config:
        model = Movie
        include = [
            'name_uk',
            'name_ru',
            'description_uk',
            'description_ru',
            'year',
            'budget',
            'duration',
            'genres',
            'released',
            'countries',
            'legal_age',
            'card_img',
            'gallery',
            'seo_title',
            'seo_image',
            'seo_description',
        ]
        optional = ['gallery', ]


class MovieCardOutSchema(ModelSchema):
    """
    Pydantic schema for showing Movie card.
    """
    banner: ImageOutSchema

    class Meta:
        model = Movie
        fields = ['name',
                  'card_img',
                  'slug', ]


class MovieOutSchema(ModelSchema):
    """
    Pydantic schema for showing Movie full data.
    """
    card_img: ImageOutSchema
    seo_image: ImageOutSchema

    @staticmethod
    def resolve_genres(obj: Movie):
        return str(obj.genres)

    @staticmethod
    def resolve_countries(obj: Movie):
        result = [country.name for country in obj.countries]

        return ', '.join(result)

    class Meta:
        model = Movie
        fields = ['name',
                  'description',
                  'gallery',
                  'slug',
                  'genres',
                  'duration',
                  'legal_age',
                  'countries',
                  'seo_title',
                  'seo_image',
                  'seo_description',
                  ]


class MovieUpdateSchema(MovieInSchema):
    """
    Pydantic schema for updating Movie.
    """

    card_img: ImageUpdateSchema = None
    seo_image: ImageUpdateSchema = None
    gallery: List[GalleryItemSchema] = None
    countries: List[CountryEnum]
    genres: List[GenresEnum]

    class Config(MovieInSchema.Config):
        include = [
            'name_uk',
            'name_ru',
            'description_uk',
            'description_ru',
            'countries',
            'duration',
            'genres',
            'gallery',
            'seo_title',
            'seo_image',
            'seo_description',
        ]
        optional = '__all__'
