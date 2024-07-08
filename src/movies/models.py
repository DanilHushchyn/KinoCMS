from django.db import models
from src.core.models import Seo
from src.movies.manager import MovieManager
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from src.movies.utils import MultiSelectField


class Tech(models.Model):
    name = models.CharField(max_length=60)
    color = models.CharField(max_length=60)

    class Meta:
        ordering = ['id',]
        verbose_name = "Tech"
        verbose_name_plural = "Techs"
        db_table = 'techs'


class MovieGenre(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "MovieGenre"
        verbose_name_plural = "MovieGenres"
        db_table = 'movie_genres'


class MovieParticipantPerson(models.Model):
    fullname = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "MovieParticipant"
        verbose_name_plural = "MovieParticipants"
        db_table = 'movie_participant_persons'


class MovieParticipantRole(models.Model):
    name = models.CharField(max_length=60, null=True)

    class Meta:
        verbose_name = "MovieParticipantRole"
        verbose_name_plural = "MovieParticipantRoles"
        db_table = 'movie_participant_roles'


# TECHS_CHOICES = [
#     ['3d', "3D"],
#     ['2d', "2D"],
#     ['imax', "IMAX"],
#     ['4dx', "4DX"],
#     ['5d', "5D"],
# ]


class MovieParticipant(models.Model):
    person = models.ForeignKey(MovieParticipantPerson,
                               on_delete=models.CASCADE,
                               null=True)
    role = models.ForeignKey(MovieParticipantRole,
                             on_delete=models.CASCADE,
                             null=True)

    class Meta:
        ordering = ['-id']
        unique_together = ('person', 'role',)
        verbose_name = "MovieParticipant"
        verbose_name_plural = "MovieParticipants"
        db_table = 'movie_participants'


class Movie(Seo):
    slug = models.SlugField(db_index=True, unique=True, null=True)
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(max_length=20_000)
    card_img = models.OneToOneField('core.Image',
                                    related_name='movie_card',
                                    on_delete=models.DO_NOTHING,
                                    null=True)

    trailer_link = models.URLField()
    year = models.PositiveIntegerField()
    budget = models.PositiveIntegerField()
    AGE_CHOICES = [
        ["+0", "+0"],
        ["+6", "+6"],
        ["+12", "+12"],
        ["+16", "+16"],
        ["+18", "+18"],
    ]
    legal_age = models.CharField(choices=AGE_CHOICES,
                                 default='+0')
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
    duration = models.DurationField()
    released = models.DateField()
    participants = models.ManyToManyField('MovieParticipant', )
    techs = models.ManyToManyField('Tech', )

    # techs = MultiSelectField(choices=TECHS_CHOICES,
    #                          min_choices=1,
    #                          max_length=255, null=True)

    genres = MultiSelectField(choices=GENRES_CHOICES,
                              min_choices=1,
                              max_length=255, null=True)
    countries = CountryField(multiple=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    gallery = models.OneToOneField('core.Gallery',
                                   on_delete=models.DO_NOTHING,
                                   null=True)
    objects = MovieManager()

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        db_table = 'movies'
