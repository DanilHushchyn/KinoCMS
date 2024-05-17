# -*- coding: utf-8 -*-
"""
    In this module described models for application users
    Their purpose is storing data for users
    and access control system in our site
    Models:
       User
       PasswordResetToken
"""
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
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
    birthday = models.DateField(null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = ['-date_joined']
        verbose_name = "Users"
        verbose_name_plural = "Users"
        db_table = "users"
