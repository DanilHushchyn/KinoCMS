"""Module for translating essences from movie app"""

from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import register

from src.movies.models import Movie
from src.movies.models import MovieParticipantPerson
from src.movies.models import MovieParticipantRole


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
