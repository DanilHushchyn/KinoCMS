# -*- coding: utf-8 -*-
from modeltranslation.translator import TranslationOptions, register

from src.movies.models import (Movie,
                               MovieParticipantPerson,
                               MovieParticipantRole)


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ("name", "description")
    required_languages = ("uk", "ru")


@register(MovieParticipantRole)
class MovieParticipantRoleTranslationOptions(TranslationOptions):
    fields = ("name",)
    required_languages = ("uk", "ru")


@register(MovieParticipantPerson)
class MovieParticipantPersonTranslationOptions(TranslationOptions):
    fields = ("fullname",)
    required_languages = ("uk", "ru")
