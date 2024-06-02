# -*- coding: utf-8 -*-
from modeltranslation.translator import TranslationOptions, register

from src.movies.models import Movie


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ("name", "description")
    required_languages = ("uk", "ru")
