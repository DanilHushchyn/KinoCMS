from django.db import models

from src.core.models import Seo
from src.movies.manager import MovieManager

from django_countries.fields import CountryField


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
    genres = models.ManyToManyField('MovieGenre')
    released = models.DateField(null=True)
    participants = models.ManyToManyField('MovieParticipant')
    COUNTRY_CHOICES = [
        [1, "Украина"],
        [2, "США"],
        [3, "Германия"],
        [4, "Франция"],
        [5, "Великобритания"],
    ]
    countries = CountryField(multiple=True, blank=True)
    gallery = models.OneToOneField('core.Gallery',
                                   on_delete=models.DO_NOTHING,
                                   null=True)
    objects = MovieManager()

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        db_table = 'movies'
