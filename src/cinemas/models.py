"""models for app cinemas"""

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from src.cinemas.managers.cinema import CinemaManager
from src.cinemas.managers.hall import HallManager
from src.core.models import Seo


# Create your models here.
class Cinema(Seo):
    """Описание Cinema.
    Наследуется от abstract model Seo, и наследует все её поля

    Дополнительная информация о модели, ее назначении и использовании.
    Таинственные поля:
    :param terms описывает условия посещения кинотеатра, они находятся
           в макете под description и хранятся в формате JSON;
    :param coordinate это ссылка на google Maps.
    :param banner,logo (OneToOneField)- поля которые
           ссылаются на model  Image и
           являются для сущности картинками
    :param gallery (OneToOneField): ссылка на сущность
           которая может хранить набор картинок,
           галерея нужна для слайдера на страницу сущности Cinema
           в самом низу макета.
    :param slug (SlugField): это поля нужно для внешнего
    уникального ключа для адрессной строки в браузере,
    генерим его на основе поля name.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, db_index=True, null=True)
    description = models.TextField(max_length=20000)
    terms = models.JSONField()
    phone_1 = PhoneNumberField()
    phone_2 = PhoneNumberField()
    email = models.EmailField()
    banner = models.OneToOneField(
        "core.Image", related_name="cin_bnr", on_delete=models.DO_NOTHING, null=True
    )
    logo = models.OneToOneField(
        "core.Image", on_delete=models.DO_NOTHING, related_name="logo", null=True
    )
    address = models.TextField(max_length=2000)
    coordinate = models.URLField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    gallery = models.OneToOneField(
        "core.Gallery", on_delete=models.DO_NOTHING, null=True
    )
    objects = CinemaManager()

    class Meta:
        ordering = [
            "-date_created",
        ]
        verbose_name = "Cinema"
        verbose_name_plural = "Cinemas"
        db_table = "cinemas"


class Hall(Seo):
    """Описание Hall.
    Наследуется от abstract model Seo, и наследует все её поля
    Является дочерней моделей для кинотеатров.
    Дополнительная информация о модели, ее назначении и использовании.
    Таинственные поля:
    :param layout описывает условия посещения кинотеатра, они находятся
           в макете под description и хранятся в формате JSON;
    :param tech поле служит для ограничения показа только одного
           формата фильма в конкретно взятом зале. Так реалистичнее
    :param banner (OneToOneField)- поле которое
           ссылаются на model  Image и
           является для сущности картинкой которая
           хранится в файловой системе проекта
    :param gallery (OneToOneField): ссылка на сущность
           которая может хранить набор картинок,
           галерея нужна для слайдера на страницу сущности Cinema
           в самом низу макета.
    :param slug (SlugField): это поля нужно для внешнего
    уникального ключа для адрессной строки в браузере,
    генерим его на основе поля name.
    """

    number = models.CharField(max_length=60)
    description = models.TextField(max_length=20_000, null=True)
    banner = models.OneToOneField(
        "core.Image", related_name="hall_bnr", on_delete=models.DO_NOTHING, null=True
    )
    layout = models.JSONField()
    date_created = models.DateTimeField(auto_now_add=True)
    cinema = models.ForeignKey("Cinema", on_delete=models.CASCADE, null=True)
    tech = models.ForeignKey("movies.Tech", on_delete=models.CASCADE, null=True)
    gallery = models.OneToOneField(
        "core.Gallery", on_delete=models.DO_NOTHING, null=True
    )
    objects = HallManager()

    class Meta:
        ordering = ["-date_created"]
        verbose_name = "Hall"
        unique_together = [
            ["cinema", "number"],
        ]
        verbose_name_plural = "Halls"
        db_table = "halls"
