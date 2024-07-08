from typing import List
from src.booking.models import Seance
from ninja import ModelSchema, FilterSchema, Schema
from pydantic import field_validator
from django.utils.translation import gettext as _
from dateutil.parser import parse
from src.core.errors import UnprocessableEntityExceptionError
from src.core.models import Image
from src.core.schemas.images import ImageOutSchema
from django.utils import timezone
from django.template.defaultfilters import date as _date
from django.utils import translation
import pymorphy2


class SeanceCardOutSchema(ModelSchema):
    """
    Pydantic schema for showing séance card.
    """
    card_img: ImageOutSchema
    banner: ImageOutSchema
    summary: str
    movie_name: str

    @staticmethod
    def resolve_card_img(obj: Seance) -> Image:
        return obj.movie.card_img

    @staticmethod
    def resolve_banner(obj: Seance) -> Image:
        return obj.hall.banner

    @staticmethod
    def resolve_movie_name(obj: Seance) -> str:
        return obj.movie.name

    @staticmethod
    def resolve_summary(obj: Seance) -> str:
        date = _date(obj.date, 'd F')
        date = date.split(' ')
        current_lang = translation.get_language()
        morph = pymorphy2.MorphAnalyzer(lang=current_lang)
        parser = morph.parse(date[1])[0]
        gent = parser.inflect({'gent'})
        date[1] = gent.word
        date = ' '.join(date).upper()
        summary = (_("{date}, {time}, ЗАЛ №{hall_number}")
                   .format(date=date, time=obj.date.strftime('%H:%M'),
                           hall_number=obj.hall.number))
        return summary

    class Meta:
        model = Seance
        fields = [
            'price',
            'hall',
            'id', ]


class SeanceShortSchema(ModelSchema):
    """
    Pydantic schema for showing séance card.
    """
    title: str

    @staticmethod
    def resolve_title(obj: Seance) -> str:
        title = (_("Сеанс - {time}")
                 .format(time=obj.date.strftime('%H:%M')))
        return title

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
    booking: bool
    time: str

    @staticmethod
    def resolve_booking(obj: Seance) -> bool:
        seats_count = obj.hall.layout['seatsCount']
        tickets_count = obj.ticket_set.count()
        if seats_count == tickets_count:
            return False
        today = timezone.now()
        if today > obj.date:
            return False
        return True

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
                  'id', ]


class ScheduleOutSchema(Schema):
    """
    Pydantic schema for showing shedule.
    """
    date: str
    seances: List[SeanceOutSchema]


class SeanceFilterSchema(FilterSchema):
    """
    Pydantic schema for getting filtered séances
    """
    cnm_slug: str
    hall_ids: List[int] = None
    mv_slugs: List[str] = None
    tech_ids: List[int] = None
    date: str = None

    @field_validator('date')
    @classmethod
    def clean_date(cls, v: str) -> str:
        try:
            result = parse(v, dayfirst=True).date()
        except ValueError as exc:
            msg = (_('Невірний формат дати було надано: {v}.'
                     'Правильний формат: 01.12.2012')
                   .format(v=v))
            raise UnprocessableEntityExceptionError(message=msg)
        today = timezone.now().date()
        if result >= today:
            return result
        else:
            msg = _('Дата повинна починатися '
                    'від сьогодні і пізніше.')
            raise UnprocessableEntityExceptionError(message=msg)
