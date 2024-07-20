"""Translate essences in app cinemas"""

from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import register

from src.cinemas.models import Cinema
from src.cinemas.models import Hall


@register(Cinema)
class CinemaTranslationOptions(TranslationOptions):
    """Translate fields from model Cinema"""

    fields = ("name", "description", "terms", "address")
    required_languages = ("uk", "ru")


@register(Hall)
class HallTranslationOptions(TranslationOptions):
    """Translate fields from model Hall"""

    fields = ("description",)
    required_languages = ("uk", "ru")
