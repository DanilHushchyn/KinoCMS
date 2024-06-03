from enum import Enum

from django.db import models

from src.core.models import Seo
from src.movies.manager import MovieManager
from django.utils.translation import gettext as _

from django_countries.fields import CountryField

from src.movies.utils import MultiSelectField


class MovieTech(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "MovieTech"
        verbose_name_plural = "MovieTechs"
        db_table = 'movie_techs'


class MovieGenre(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "MovieGenre"
        verbose_name_plural = "MovieGenres"
        db_table = 'movie_genres'


class MovieParticipantPerson(models.Model):
    fullname = models.CharField(max_length=255)

    class Meta:
        verbose_name = "MovieParticipant"
        verbose_name_plural = "MovieParticipants"
        db_table = 'movie_participant_persons'


class MovieParticipantRole(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "MovieParticipantRole"
        verbose_name_plural = "MovieParticipantRoles"
        db_table = 'movie_participant_roles'


class MovieParticipant(models.Model):
    person = models.ForeignKey(MovieParticipantPerson,
                               on_delete=models.CASCADE,
                               null=True)
    role = models.ForeignKey(MovieParticipantRole,
                             on_delete=models.CASCADE,
                             null=True)

    class Meta:
        verbose_name = "MovieParticipant"
        verbose_name_plural = "MovieParticipants"
        db_table = 'movie_participants'


# class Genres(Enum):
#     COMEDY = ('comedy', _('Комедія'))
#     FANTASY = ('fantasy', _('Фантастика'))
#     HORROR = ('horror', _('Жахи'))
#     ACTION = ('action', _('Бойовик'))
#     MELODRAMAS = ('melodramas', _('Мелодрами'))
#     THRILLER = ('thriller', _('Трилер'))
#     MYSTICISM = ('mysticism', _('Містика'))
#     DETECTIVE = ('detective', _('Детектив'))
#
#     @classmethod
#     def choices(cls):
#         return tuple((i.value, i.name) for i in cls)


class Movie(Seo):
    slug = models.SlugField(db_index=True, unique=True, null=True)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=2000)
    card_img = models.OneToOneField('core.Image',
                                    related_name='movie_card',
                                    on_delete=models.DO_NOTHING,
                                    null=True)

    trailer_link = models.URLField(null=True)
    year = models.PositiveIntegerField(null=True)
    budget = models.PositiveIntegerField(null=True)
    AGE_CHOICES = [
        ["+0", "+0"],
        ["+6", "+6"],
        ["+12", "+12"],
        ["+16", "+16"],
        ["+18", "+18"],
    ]
    legal_age = models.CharField(null=True, choices=AGE_CHOICES,
                                 default='+0')
    duration = models.DurationField(null=True)
    techs = models.ManyToManyField('MovieTech')
    released = models.DateField(null=True)
    participants = models.ManyToManyField('MovieParticipant')
    GENRES_CHOICES = [
        ['comedy', _("Комедія")],
        ['fantasy', _("Фантастика")],
        ['horror', _("Жахи")],
        ['action', _("Бойовик")],
        ['melodramas', _("Мелодрами")],
        ['thriller', _("Трилер")],
        ['mysticism', _("Містика")],
        ['detective', _("Детектив")],
    ]
    genres = MultiSelectField(choices=GENRES_CHOICES,
                              min_choices=1,
                              max_length=255, null=True)
    countries = CountryField(multiple=True, blank=True)
    gallery = models.OneToOneField('core.Gallery',
                                   on_delete=models.DO_NOTHING,
                                   null=True)
    objects = MovieManager()

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        db_table = 'movies'
