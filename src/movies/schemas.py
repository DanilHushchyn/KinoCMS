import datetime
from enum import Enum
from typing import List
import ninja_schema
from pydantic.fields import Field
from src.core.errors import (UnprocessableEntityExceptionError,
                             NotFoundExceptionError)
from src.movies.models import (Movie, MovieParticipant,
                               MovieParticipantRole, Tech)
from ninja import ModelSchema
from django.utils.translation import gettext as _
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import (ImageOutSchema, ImageInSchema,
                                     ImageUpdateSchema)
from django_countries.data import COUNTRIES
from pydantic import field_validator
from django.utils import timezone

from dateutil.parser import parse

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


class ReleaseEnum(Enum):
    Soon = "soon"
    Current = "current"

    @classmethod
    def _missing_(cls, value):
        return cls.Current


def current_year():
    return datetime.date.today().year


class TechOutSchema(ModelSchema):
    """
    Pydantic schema for showing Movie techs.
    """

    class Meta:
        model = Tech
        fields = ['name',
                  'color',
                  'id', ]


class MovieInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for creating Movies to server side.
    """

    card_img: ImageInSchema
    seo_image: ImageInSchema
    gallery: List[ImageInSchema] = None
    countries: List[CountryEnum]
    genres: List[GenresEnum]
    name_uk: str = Field(max_length=60)
    name_ru: str = Field(max_length=60)
    description_uk: str = Field(max_length=2000)
    description_ru: str = Field(max_length=2000)
    released: str

    @field_validator('released')
    @classmethod
    def clean_released(cls, v: str) -> str:
        try:
            result = parse(v, dayfirst=True).date()
        except ValueError as exc:
            msg = _('Невірний формат дати було надано: {v}. '
                    'Правильний формат: 01.12.2012').format(v=v)
            raise UnprocessableEntityExceptionError(message=msg, field='released')
        today = timezone.now().date()
        if result >= today:
            return result
        else:
            msg = _('Дата повинна починатися '
                    'від сьогодні і пізніше.')
            raise UnprocessableEntityExceptionError(message=msg, field='released')

    @ninja_schema.model_validator('year')
    def clean_year(cls, year) -> int:
        if year < 1984 or year > current_year() + 1:
            msg = (_('Очікуваний мінімальний рік становить {min}, '
                     'максимальний рік {max} '
                     'but got {current}')
                   .format(min=1984, max=current_year() + 1,
                           current=year))
            raise UnprocessableEntityExceptionError(message=msg)
        return year

    @ninja_schema.model_validator('genres')
    def clean_genres(cls, genres) -> List[str]:
        genres = set(genres)
        result = []
        keys = [str(key) for key, value in Movie.GENRES_CHOICES]
        for genre in genres:
            if genre not in keys:
                msg = (_('Список має складатися з наступних значень {keys}')
                       .format(keys=keys))
                raise UnprocessableEntityExceptionError(message=msg)
            result.append(genre.value)
        return result

    @ninja_schema.model_validator('countries')
    def clean_countries(cls, countries) -> List[str]:
        countries = set(countries)
        result = []
        for country in countries:
            if country not in COUNTRIES.keys():
                msg = (_('Список має складатися з наступних значень {keys}')
                       .format(keys=list(COUNTRIES.keys())))
                raise UnprocessableEntityExceptionError(message=msg)
            result.append(country.value)
        return result

    @ninja_schema.model_validator('participants')
    def clean_participants(cls, participant_ids: List[int]) -> List[int]:
        participants_db = list(MovieParticipant.objects
                               .filter(id__in=participant_ids)
                               .values_list('id', flat=True))
        if len(participant_ids) != len(participants_db):
            diff = list(set(participant_ids) ^ set(participants_db))
            msg = (_('У заданому переліку участників є '
                     'ids {diff} які не присутні у базі')
                   .format(diff=diff))
            raise NotFoundExceptionError(message=msg,
                                         cls_model=MovieParticipant,
                                         field='participants')
        return participant_ids

    @ninja_schema.model_validator('techs')
    def clean_techs(cls, tech_ids: List[int]) -> List[int]:
        techs_db = list(Tech.objects
                        .filter(id__in=tech_ids)
                        .values_list('id', flat=True))
        if len(tech_ids) != len(techs_db):
            diff = list(set(tech_ids) ^ set(techs_db))
            msg = (_('У заданому переліку технологій є '
                     'ids {diff} які не присутні у базі')
                   .format(diff=diff))
            raise NotFoundExceptionError(message=msg,
                                         cls_model=Tech,
                                         field='techs')
        return tech_ids

    class Config:
        model = Movie
        include = [
            'name_uk',
            'name_ru',
            'description_uk',
            'description_ru',
            'year',
            'released',
            'budget',
            'duration',
            'genres',
            'participants',
            'countries',
            'techs',
            'trailer_link',
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
    card_img: ImageOutSchema
    techs: List[TechOutSchema]
    released: str

    @staticmethod
    def resolve_released(obj: Movie) -> str:
        released = obj.released.strftime("%d.%m.%Y")
        return released

    class Meta:
        model = Movie
        fields = ['name',
                  'legal_age',
                  'card_img',
                  'released',
                  'slug', ]


class MovieScheduleFilterSchema(ModelSchema):
    """
    Pydantic schema for showing Movie card.
    """

    class Meta:
        model = Movie
        fields = ['name',
                  'slug', ]


class MovieOutSchema(ModelSchema):
    """
    Pydantic schema for showing Movie full data.
    """
    card_img: ImageOutSchema
    seo_image: ImageOutSchema
    genres: List[str]
    techs: List[TechOutSchema]
    countries: List[str]
    released: str

    @staticmethod
    def resolve_released(obj: Movie) -> str:
        released = obj.released.strftime("%d.%m.%Y")
        return released

    @staticmethod
    def resolve_genres(obj: Movie) -> List[str]:
        result = []
        for genre in obj.genres:
            result.append(genre)
        return result

    @staticmethod
    def resolve_legal_age(obj: Movie) -> str:
        legal_age_display = dict(Movie.AGE_CHOICES)[obj.legal_age]
        return legal_age_display

    @staticmethod
    def resolve_countries(obj: Movie) -> List[str]:
        result = []
        for country in obj.countries:
            result.append(country.code)
        return result

    class Meta:
        model = Movie
        fields = ['name_uk',
                  'name_ru',
                  'description_uk',
                  'description_ru',
                  'gallery',
                  'slug',
                  'genres',
                  'duration',
                  'legal_age',
                  'trailer_link',
                  'year',
                  'techs',
                  'released',
                  'budget',
                  'participants',
                  'countries',
                  'seo_title',
                  'seo_image',
                  'seo_description',
                  ]


class MovieParticipantClientOutSchema(ModelSchema):
    """
    Pydantic schema for showing Participants of movie
    """
    person: str
    role: str

    @staticmethod
    def resolve_person(obj: MovieParticipant) -> str:
        return str(obj.person.fullname)

    @staticmethod
    def resolve_role(obj: MovieParticipant) -> str:
        return str(obj.role.name)

    class Meta:
        model = MovieParticipant
        fields = ['person', ]


class MovieRolesClientOutSchema(ModelSchema):
    """
    Pydantic schema for showing Participants of movie
    """
    persons: List[str]

    class Meta:
        model = MovieParticipantRole
        fields = ['name', ]


class MovieClientOutSchema(ModelSchema):
    """
    Pydantic schema for showing Movie full data.
    """
    card_img: ImageOutSchema
    seo_image: ImageOutSchema
    genres_display: str
    countries_display: str
    techs: List[TechOutSchema]
    mv_roles: List[MovieRolesClientOutSchema]
    released: str

    @staticmethod
    def resolve_released(obj: Movie) -> str:
        released = obj.released.strftime("%d.%m.%Y")
        return released

    @staticmethod
    def resolve_legal_age(obj: Movie) -> str:
        legal_age_display = dict(Movie.AGE_CHOICES)[obj.legal_age]
        return legal_age_display

    @staticmethod
    def resolve_genres_display(obj: Movie) -> str:
        return str(obj.genres)

    @staticmethod
    def resolve_countries_display(obj: Movie) -> str:
        result = [country.name for country in obj.countries]
        return ', '.join(result)

    class Meta:
        model = Movie
        fields = ['name',
                  'description',
                  'gallery',
                  'slug',
                  'card_img',
                  'duration',
                  'trailer_link',
                  'legal_age',
                  'year',
                  'budget',
                  'released',
                  'seo_title',
                  'seo_image',
                  'seo_description',
                  ]


class MovieUpdateSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for updating Movie.
    """

    card_img: ImageUpdateSchema = None
    seo_image: ImageUpdateSchema = None
    gallery: List[GalleryItemSchema] = None
    countries: List[CountryEnum] = None
    genres: List[GenresEnum] = None

    @ninja_schema.model_validator('year')
    def clean_year(cls, year) -> int:
        if year < 1984 or year > current_year() + 1:
            msg = (_('Очікуваний мінімальний рік становить {min}, '
                     'максимальний рік {max} '
                     'але отримано {current}')
                   .format(min=1984, max=current_year() + 1,
                           current=year))
            raise UnprocessableEntityExceptionError(message=msg)
        return year

    @ninja_schema.model_validator('genres')
    def clean_genres(cls, genres) -> List[str]:
        genres = set(genres)
        result = []
        keys = [str(key) for key, value in Movie.GENRES_CHOICES]
        for genre in genres:
            if genre not in keys:
                msg = (_('Список має складатися з наступних значень {keys}')
                       .format(keys=keys))
                raise UnprocessableEntityExceptionError(message=msg)
            result.append(genre.value)
        return result

    @ninja_schema.model_validator('countries')
    def clean_countries(cls, countries) -> List[str]:
        countries = set(countries)
        result = []
        for country in countries:
            if country not in COUNTRIES.keys():
                msg = (_('Список має складатися з наступних значень '
                         '{keys}').format(keys=list(COUNTRIES.keys())))
                raise UnprocessableEntityExceptionError(message=msg)
            result.append(country.value)
        return result

    @ninja_schema.model_validator('participants')
    def clean_participants(cls, participant_ids: List[int]) -> List[int]:
        participants_db = list(MovieParticipant.objects
                               .filter(id__in=participant_ids)
                               .values_list('id', flat=True))
        if len(participant_ids) != len(participants_db):
            diff = list(set(participant_ids) ^ set(participants_db))
            msg = (_('У заданому переліку участників є '
                     'ids {diff} які не присутні у базі')
                   .format(diff=diff))
            raise NotFoundExceptionError(message=msg,
                                         cls_model=MovieParticipant,
                                         field='participants')
        return participant_ids

    class Config:
        model = Movie
        include = [
            'name_uk',
            'name_ru',
            'description_uk',
            'description_ru',
            'countries',
            'duration',
            'budget',
            'year',
            'trailer_link',
            'participants',
            'genres',
            'gallery',
            'seo_title',
            'seo_image',
            'seo_description',
        ]
        optional = "__all__"


class MovieParticipantOutSchema(ModelSchema):
    """
    Pydantic schema for getting
    all movie participants in system.
    """

    display: str

    @staticmethod
    def resolve_display(obj: MovieParticipant) -> str:
        return obj.person.fullname + ' - ' + obj.role.name

    class Meta:
        model = MovieParticipant
        fields = [
            'id',
        ]


class MovieParticipantSelectOutSchema(ModelSchema):
    """
    Pydantic schema for getting
    all movie participants in system.
    """
    name: str

    @staticmethod
    def resolve_name(obj: MovieParticipant) -> str:
        return obj.person.fullname

    class Meta:
        model = MovieParticipant
        fields = [
            'id',
        ]


class MovieParticipantRoleOutSchema(ModelSchema):
    """
    Pydantic schema for getting
    all movie participants in system grouped by role.
    """

    persons: List[MovieParticipantSelectOutSchema]

    class Meta:
        model = MovieParticipantRole
        fields = [
            'name',
        ]


class MovieSearchOutSchema(ModelSchema):
    """
    Pydantic schema for searching movies in site.
    """
    card_img: ImageOutSchema

    class Meta:
        model = Movie
        fields = ['name',
                  'card_img',
                  'slug'
                  ]
