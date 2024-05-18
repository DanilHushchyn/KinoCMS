# -*- coding: utf-8 -*-
"""
    In this module described models for application users
    Their purpose is storing data for users
    and access control system in our site
"""
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from src.users.managers.user_manager import CustomUserManager


class User(AbstractUser):
    """
    This is our Auth Model in the site
    It's stores all data about users and provides
    some methods for creating users
    """

    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    nickname = models.CharField(max_length=255, null=True)
    username = (None,)
    man = models.BooleanField(default=True)
    phone_number = PhoneNumberField(null=True)
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(max_length=255, null=True)
    CITIES_CHOICES = [
      ["0", _("Інше")],
      ["1", _("Київ")],
      ["2", _("Харків")],
      ["3", _("Одеса")],
      ["4", _("Дніпро")],
      ["5", _("Донецьк")],
      ["6", _("Запоріжжя")],
      ["7", _("Львів")],
      ["8", _("Кривий Ріг")],
      ["9", _("Миколаїв")],
      ["10", _("Вінниця")],
      ["11", _("Луганськ")],
      ["12", _("Сімферополь")],
      ["13", _("Херсон")],
      ["14", _("Полтава")],
      ["15", _("Чернігів")],
      ["16", _("Черкаси")],
      ["17", _("Житомир")],
      ["18", _("Суми")],
      ["19", _("Хмельницький")],
      ["20", _("Чернівці")],
      ["21", _("Рівне")],
      ["22", _("Івано-Франківськ")],
      ["23", _("Тернопіль")],
      ["24", _("Луцьк")],
    ]

    city = models.CharField(max_length=255, choices=CITIES_CHOICES, default=0)
    birthday = models.DateField(null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = ['-date_joined']
        verbose_name = "Users"
        verbose_name_plural = "Users"
        db_table = "users"
