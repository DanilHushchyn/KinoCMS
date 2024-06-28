# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "users".

implement logic for encoding and decoding data into python
object and json
"""
import enum
import re
from phonenumber_field.validators import (
    validate_international_phonenumber)
from django.core.exceptions import ValidationError
import ninja_schema
from ninja import ModelSchema
from pydantic.types import SecretStr
from src.core.errors import UnprocessableEntityExceptionError
from src.users.models import User
from django.utils.translation import gettext as _


class UserFieldsEnum(enum.Enum):
    id = "id"
    date_joined = "date_joined"
    birthday = "birthday"
    email = "email"
    phone_number = "phone_number"
    fio = "fio"
    nickname = "nickname"
    city = "city"


class UserInBaseSchema(ninja_schema.ModelSchema):
    """
    Pydantic base schema with data from outside for User.

    Purpose of this schema to get user's
    personal data for system purposes
    """

    class Config:
        model = User
        include = [
            "first_name",
            "last_name",
            "nickname",
            "city",
            "man",
            "phone_number",
            "email",
            "address",
            "birthday", ]

    @staticmethod
    def validate_fio(fio: str) -> bool:
        pattern = r"^[A-ZА-ЯЇІЄҐ][a-zа-яїієґ'-]+$"
        if fio is None or re.match(pattern, fio):
            return True
        else:
            return False

    @ninja_schema.model_validator('phone_number')
    def validate_phone_number(cls, value) -> str:
        try:
            validate_international_phonenumber(value)
        except ValidationError:
            msg = _("Введено некоректний номер телефону.")
            raise UnprocessableEntityExceptionError(message=msg)

        return value

    @ninja_schema.model_validator('city')
    def clean_city(cls, city) -> str:
        return city.value

    @ninja_schema.model_validator('first_name')
    def clean_first_name(cls, value) -> str:
        if not cls.validate_fio(value):
            msg = _("Ім'я повинно починатися з великої літери"
                    "(наступні маленькі), доступна кирилиця та латиниця, "
                    "доступні спецсимволи('-)")
            raise UnprocessableEntityExceptionError(msg)
        return value

    @ninja_schema.model_validator('last_name')
    def clean_last_name(cls, value) -> str:
        if not cls.validate_fio(value):
            msg = _("Прізвище повинно починатися з великої літери"
                    "(наступні маленькі), доступна кирилиця та латиниця, "
                    "доступні спецсимволи('-)")
            raise UnprocessableEntityExceptionError(msg)
        return value


class UserRegisterSchema(UserInBaseSchema):
    """
    Pydantic schema for User.

    Purpose of this schema to get user's
    personal data for registration
    """
    password1: SecretStr
    password2: SecretStr

    @staticmethod
    def check_password(password: str) -> None:
        password_pattern = ("^(?=.*?[A-Z])(?=.*?[a-z])"
                            "(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
        if re.match(password_pattern, password) is None:
            msg = _(
                "Пароль повинен відповідати: "
                "* Хоча б одній великій літері, "
                "* Хоча б одній малій літері, "
                "* Хоча б одній цифрі, "
                "* Хоча б одному спеціальному символу з набору ?!@%^&- "
                "* Мінімальна довжина 8 символів"
            )
            raise UnprocessableEntityExceptionError(msg)

    @ninja_schema.model_validator('password1')
    def clean_password1(cls, password1: SecretStr) -> SecretStr:
        password = password1.get_secret_value()
        cls.check_password(password)
        return password1

    @ninja_schema.model_validator('password2')
    def clean_password2(cls, password2: SecretStr) -> SecretStr:
        password = password2.get_secret_value()
        cls.check_password(password)
        return password2


class UserUpdateSchema(UserInBaseSchema):
    """
    Pydantic schema for update User.

    Purpose of this schema to get user's
    personal data for updating
    """

    password: SecretStr = None

    @staticmethod
    def check_password(password: str) -> None:
        password_pattern = ("^(?=.*?[A-Z])(?=.*?[a-z])"
                            "(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
        if re.match(password_pattern, password) is None:
            msg = _(
                "Пароль повинен відповідати: "
                "* Хоча б одній великій літері, "
                "* Хоча б одній малій літері, "
                "* Хоча б одній цифрі, "
                "* Хоча б одному спеціальному символу з набору ?!@%^&- "
                "* Мінімальна довжина 8 символів"
            )
            raise UnprocessableEntityExceptionError(msg)

    @ninja_schema.model_validator('password')
    def clean_password(cls, password: SecretStr) -> SecretStr:
        value = password.get_secret_value()
        cls.check_password(value)
        return password

    class Config(UserInBaseSchema.Config):
        optional = "__all__"


class UserOutSchema(ModelSchema):
    """
    Pydantic schema for User.

    Purpose of this schema to return user's
    personal data
    """

    city_display: str
    date_joined: str
    birthday: str

    @staticmethod
    def resolve_city_display(obj: User):
        return _(obj.get_city_display())

    @staticmethod
    def resolve_phone_number(obj: User):
        return str(obj.phone_number)

    @staticmethod
    def resolve_date_joined(obj: User):
        dj = obj.date_joined.strftime("%d.%m.%Y")
        return dj

    @staticmethod
    def resolve_birthday(obj: User):
        birth = obj.birthday.strftime("%d.%m.%Y")
        return birth

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "nickname",
            "date_joined",
            "city",
            "man",
            "phone_number",
            "email",
            "address",
            "is_superuser",
            "birthday", ]
