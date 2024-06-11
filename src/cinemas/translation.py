# -*- coding: utf-8 -*-
from modeltranslation.translator import TranslationOptions, register

from src.cinemas.models import Cinema, Hall


@register(Cinema)
class CinemaTranslationOptions(TranslationOptions):
    fields = ("name", "description", "terms", 'address')
    required_languages = ("uk", "ru")


@register(Hall)
class CinemaTranslationOptions(TranslationOptions):
    fields = ("description",)
    required_languages = ("uk", "ru")
