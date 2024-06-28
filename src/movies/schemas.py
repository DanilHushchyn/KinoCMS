import datetime
from enum import Enum
from typing import List
import ninja_schema
from pydantic.fields import Field
from src.core.errors import UnprocessableEntityExceptionError, NotFoundExceptionError
from src.movies.models import Movie, MovieParticipant, TECHS_CHOICES
from ninja import ModelSchema
from django.utils.translation import gettext as _
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageOutSchema, ImageInSchema, ImageUpdateSchema
from django_countries.data import COUNTRIES

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
TechsEnum = Enum(
    "TechsEnum",
    [(value, key) for key, value in TECHS_CHOICES],
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


class MovieInSchema(ninja_schema.ModelSchema):
    """
    Pydantic schema for creating Movies to server side.
    """

    card_img: ImageInSchema
    seo_image: ImageInSchema
    gallery: List[ImageInSchema] = None
    countries: List[CountryEnum]
    genres: List[GenresEnum]
    techs: List[TechsEnum]
    name_uk: str = Field(max_length=60)
    name_ru: str = Field(max_length=60)
    description_uk: str = Field(max_length=2000)
    description_ru: str = Field(max_length=2000)

    @ninja_schema.model_validator('year')
    def clean_year(cls, year) -> int:
        if year < 1984 or year > current_year() + 1:
            msg = _(f'Expected min year is 1984 '
                    f'max year is {current_year() + 1} '
                    f'but got {year}')
            raise UnprocessableEntityExceptionError(message=msg)
        return year

    @ninja_schema.model_validator('genres')
    def clean_genres(cls, genres) -> List[str]:
        genres = set(genres)
        result = []
        keys = [str(key) for key, value in Movie.GENRES_CHOICES]
        for genre in genres:
            if genre not in keys:
                msg = _(f'List should contain any of '
                        f'{keys}')
                raise UnprocessableEntityExceptionError(message=msg)
            result.append(genre.value)
        return result

    @ninja_schema.model_validator('techs')
    def clean_techs(cls, techs) -> List[str]:
        techs = set(techs)
        result = []
        keys = [str(key) for key, value in TECHS_CHOICES]
        for tech in techs:
            if tech not in keys:
                msg = _(f'List should contain any of '
                        f'{keys}')
                raise UnprocessableEntityExceptionError(message=msg)
            result.append(tech.value)
        return list(result)

    @ninja_schema.model_validator('countries')
    def clean_countries(cls, countries) -> List[str]:
        countries = set(countries)
        result = []
        for country in countries:
            if country not in COUNTRIES.keys():
                msg = _(f'List should contain any of '
                        f'{list(COUNTRIES.keys())}')
                raise UnprocessableEntityExceptionError(message=msg)
            result.append(country.value)
        return result

    @ninja_schema.model_validator('participants')
    def clean_participants(cls, participants) -> List[int]:
        participants = set(participants)
        participants_ids = (MovieParticipant.objects
                            .values_list('id', flat=True))
        for participant in participants:
            if participant not in participants_ids:
                msg = _(f'Not Found: No MovieParticipant'
                        f'matches the given id - {participant}')
                raise NotFoundExceptionError(message=msg)
        return list(participants)

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
            'released',
            'countries',
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

    class Meta:
        model = Movie
        fields = ['name',
                  'legal_age',
                  'card_img',
                  'released',
                  'slug', ]


class MovieOutSchema(ModelSchema):
    """
    Pydantic schema for showing Movie full data.
    """
    card_img: ImageOutSchema
    seo_image: ImageOutSchema
    genres_display: str
    genres: List[str]
    techs: List[str]
    countries: List[str]
    countries_display: str
    techs_display: str

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
    def resolve_techs(obj: Movie) -> List[str]:
        result = []
        for tech in obj.techs:
            result.append(tech)
        return result

    @staticmethod
    def resolve_genres_display(obj: Movie) -> str:
        return str(obj.genres)

    @staticmethod
    def resolve_techs_display(obj: Movie) -> str:
        return str(obj.techs)

    @staticmethod
    def resolve_countries(obj: Movie) -> List[str]:
        result = []
        for country in obj.countries:
            result.append(country.code)
        return result

    @staticmethod
    def resolve_countries_display(obj: Movie) -> str:
        result = [country.name for country in obj.countries]
        return ', '.join(result)

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
        fields = ['person',
                  'role', ]


class MovieClientOutSchema(ModelSchema):
    """
    Pydantic schema for showing Movie full data.
    """
    card_img: ImageOutSchema
    seo_image: ImageOutSchema
    genres_display: str
    countries_display: str
    techs_display: str
    participants: List[MovieParticipantClientOutSchema]

    @staticmethod
    def resolve_legal_age(obj: Movie) -> str:
        legal_age_display = dict(Movie.AGE_CHOICES)[obj.legal_age]
        return legal_age_display

    @staticmethod
    def resolve_genres_display(obj: Movie) -> str:
        return str(obj.genres)

    @staticmethod
    def resolve_techs_display(obj: Movie) -> str:
        return str(obj.techs)

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
                  'participants',
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
    countries: List[CountryEnum] = None
    genres: List[GenresEnum] = None
    techs: List[TechsEnum] = None

    class Config(MovieInSchema.Config):
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
            'released',
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
