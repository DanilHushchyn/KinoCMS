"""In this module described models for application users
Their purpose is storing data for users
and access control system in our site
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from src.users.managers.user_manager import CustomUserManager


class User(AbstractUser):
    """This is our Auth Model in the site
    It's stores all data about users and provides
    some methods for creating users
    """

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    username = (None,)
    man = models.BooleanField()
    phone_number = PhoneNumberField()
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    CITIES_CHOICES = [
        ["інше", _("Інше")],
        ["київ", _("Київ")],
        ["харків", _("Харків")],
        ["одеса", _("Одеса")],
        ["дніпро", _("Дніпро")],
        ["донецьк", _("Донецьк")],
        ["запоріжжя", _("Запоріжжя")],
        ["львів", _("Львів")],
        ["кривий ріг", _("Кривий Ріг")],
        ["миколаїв", _("Миколаїв")],
        ["вінниця", _("Вінниця")],
        ["луганськ", _("Луганськ")],
        ["сімферополь", _("Сімферополь")],
        ["херсон", _("Херсон")],
        ["полтава", _("Полтава")],
        ["чернігів", _("Чернігів")],
        ["черкаси", _("Черкаси")],
        ["житомир", _("Житомир")],
        ["суми", _("Суми")],
        ["хмельницький", _("Хмельницький")],
        ["чернівці", _("Чернівці")],
        ["рівне", _("Рівне")],
        ["івано-франківськ", _("Івано-Франківськ")],
        ["тернопіль", _("Тернопіль")],
        ["луцьк", _("Луцьк")],
    ]
    city = models.CharField(max_length=255, choices=CITIES_CHOICES)
    birthday = models.DateField()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "Users"
        verbose_name_plural = "Users"
        db_table = "users"
