from typing import List, Any
import ninja_schema
from ninja.errors import HttpError
from phonenumber_field.validators import validate_international_phonenumber
from pydantic.fields import Field
from src.booking.models import Seance
from ninja import ModelSchema, Schema
from django.utils.translation import gettext as _
from src.core.schemas.gallery import GalleryItemSchema
from src.core.schemas.images import ImageOutSchema, ImageInSchema, ImageUpdateSchema
from pydantic import Json
from django.core.exceptions import ValidationError

from src.core.utils import paginate


class SeanceCardOutSchema(ModelSchema):
    """
    Pydantic schema for showing séance card.
    """
    time: str

    @staticmethod
    def resolve_time(obj: Seance) -> str:
        return obj.date.strftime('%H:%M')

    class Meta:
        model = Seance
        fields = [
            'id', ]


class SeanceOutSchema(ModelSchema):
    """
    Pydantic schema for showing séance card.
    """
    movie_name: str
    hall_number: str
    time: str

    @staticmethod
    def resolve_movie_name(obj: Seance) -> str:
        return obj.movie.name

    @staticmethod
    def resolve_hall_number(obj: Seance) -> str:
        return obj.hall.number

    @staticmethod
    def resolve_time(obj: Seance) -> str:
        return obj.date.strftime('%H:%M')

    class Meta:
        model = Seance
        fields = ['price',
                  'date',
                  'hall',
                  'id', ]


class ScheduleOutSchema(Schema):
    """
    Pydantic schema for showing séance card.
    """
    date: str
    seances: List[SeanceOutSchema]

    @staticmethod
    def resolve_seances(obj: Seance) -> str:
        return paginate(obj.seances)
