"""Models for movie app"""

from django.db import models
from django.utils.translation import gettext as _
from django_countries.fields import CountryField

from src.core.models import Seo
from src.movies.manager import MovieManager
from src.movies.utils import MultiSelectField


class Tech(models.Model):
    """Описание Tech
    Модель хранит все технологии в которых
    показывают фильм в кинотеатрах сайта
    """

    name = models.CharField(max_length=60)
    color = models.CharField(max_length=60)

    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "Tech"
        verbose_name_plural = "Techs"
        db_table = "techs"


class MovieGenre(models.Model):
    """Описание MovieGenre
    Модель хранит все жанры фильмов
    """

    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "MovieGenre"
        verbose_name_plural = "MovieGenres"
        db_table = "movie_genres"


class MovieParticipantPerson(models.Model):
    """Описание MovieParticipantPerson
    Модель хранит людей которые связано с кино
    """

    fullname = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "MovieParticipant"
        verbose_name_plural = "MovieParticipants"
        db_table = "movie_participant_persons"


class MovieParticipantRole(models.Model):
    """Описание MovieParticipantRole
    Модель хранит список киношных профессий
    """

    name = models.CharField(max_length=60, null=True)

    class Meta:
        verbose_name = "MovieParticipantRole"
        verbose_name_plural = "MovieParticipantRoles"
        db_table = "movie_participant_roles"


class MovieParticipant(models.Model):
    """Описание MovieParticipant
    Модель является соединительной таблицей в базе
    между людьми и профессиями, обусловлено это условиями реализации
    """

    person = models.ForeignKey(
        MovieParticipantPerson, on_delete=models.CASCADE, null=True
    )
    role = models.ForeignKey(MovieParticipantRole, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-id"]
        unique_together = (
            "person",
            "role",
        )
        verbose_name = "MovieParticipant"
        verbose_name_plural = "MovieParticipants"
        db_table = "movie_participants"


class Movie(Seo):
    """Описание Movie
    Модель хранит все фильмы в системе и при содании фильма
    в соответсвующем сервисе, создаётся спиок сеансов
    Таинственные поля:
    :param slug (SlugField): это поля нужно для внешнего
            уникального ключа для адрессной строки в браузере,
            генерим его на основе поля name.
    :param trailer_link это ссылка на трейлер на её основе делается
           iframe на фронте.
    :param card_img (OneToOneField) - поле которое
           ссылаются на model  Image и
           является для сущности картинкой которая
           хранится в файловой системе проекта
    :param genres (MultiSelectField): хранит список из жанров
           присущих фильму благодаря свойствам поля MultiSelectField
    :param duration (DurationField): хранит время длитеьности фильма
    :param released (DateField): хранит дату предстоящего релиза фильма в кинотеатре
    :param legal_age (DateField): хранит возрастное ограничение на просмотр
    :param countries (CountryField): хранит список из стран
           причастных к созданию фильма благодаря свойствам поля CountryField
    :param participants (ManyToManyField): хранит список из людей(MovieParticipants)
           причастных к созданию фильма благодаря свойствам поля CountryField
    :param gallery (OneToOneField): ссылка на сущность
           которая может хранить набор картинок,
           галерея нужна для слайдера на страницу сущности Cinema
           в самом низу макета.
    :param slug (SlugField): это поля нужно для внешнего
    """

    slug = models.SlugField(db_index=True, unique=True, null=True)
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(max_length=20_000)
    card_img = models.OneToOneField(
        "core.Image", related_name="movie_card", on_delete=models.DO_NOTHING, null=True
    )

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
    legal_age = models.CharField(choices=AGE_CHOICES, default="+0")
    GENRES_CHOICES = [
        ["comedy", _("Комедія")],
        ["fantasy", _("Фантастика")],
        ["horror", _("Жахи")],
        ["action", _("Бойовик")],
        ["melodramas", _("Мелодрами")],
        ["thriller", _("Трилер")],
        ["mysticism", _("Містика")],
        ["detective", _("Детектив")],
    ]
    duration = models.DurationField()
    released = models.DateField()
    participants = models.ManyToManyField(
        "MovieParticipant",
    )
    techs = models.ManyToManyField(
        "Tech",
    )
    genres = MultiSelectField(
        choices=GENRES_CHOICES, min_choices=1, max_length=255, null=True
    )
    countries = CountryField(multiple=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    gallery = models.OneToOneField(
        "core.Gallery", on_delete=models.DO_NOTHING, null=True
    )
    objects = MovieManager()

    class Meta:
        ordering = ["-date_created"]
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        db_table = "movies"
