"""This module contains pydantic schemas for app "users".

implement logic for encoding and decoding data into python
object and json
"""

import enum
import re

import ninja_schema
from dateutil.parser import parse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from ninja import ModelSchema
from phonenumber_field.validators import validate_international_phonenumber
from pydantic import field_validator
from pydantic.types import SecretStr

from src.core.errors import UnprocessableEntityExceptionError
from src.users.models import User


class UserFieldsEnum(enum.Enum):
    """Enum for filtering datable"""

    id = "id"
    date_joined = "date_joined"
    birthday = "birthday"
    email = "email"
    phone_number = "phone_number"
    fio = "fio"
    nickname = "nickname"
    city = "city"


class UserInBaseSchema(ninja_schema.ModelSchema):
    """Pydantic base schema with data from outside for User.

    Purpose of this schema to get user's
    personal data for system purposes
    """

    birthday: str

    @field_validator("birthday")
    @classmethod
    def clean_birthday(cls, v: str) -> str:
        try:
            result = parse(v, dayfirst=True).date()
        except ValueError:
            msg = _(
                "Невірний формат дати було надано: {v}. "
                "Правильний формат: 01.12.2012"
            ).format(v=v)
            raise UnprocessableEntityExceptionError(message=msg)

        return result

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
            "birthday",
        ]

    @staticmethod
    def validate_fio(fio: str) -> bool:
        """Helps to validate field fio
        :param fio: fio
        :return: fio
        """
        pattern = r"^[A-ZА-ЯЇІЄҐ][a-zа-яїієґ'-]+$"
        if fio is None or re.match(pattern, fio):
            return True
        else:
            return False

    @ninja_schema.model_validator("phone_number")
    def validate_phone_number(cls, value) -> str:
        """Helps to validate field fio
        :param value: phone_number
        :return: phone_number
        """
        try:
            validate_international_phonenumber(value)
        except ValidationError:
            msg = _("Введено некоректний номер телефону.")
            raise UnprocessableEntityExceptionError(message=msg)

        return value

    @ninja_schema.model_validator("city")
    def clean_city(cls, city) -> str:
        """Helps to validate field city
        :param city: city
        :return: city
        """
        return city.value

    @ninja_schema.model_validator("first_name")
    def clean_first_name(cls, value) -> str:
        """Helps to validate field first_name
        :param value: first_name
        :return: first_name
        """
        if not cls.validate_fio(value):
            msg = _(
                "Ім'я повинно починатися з великої літери"
                "(наступні маленькі), доступна кирилиця та латиниця, "
                "доступні спецсимволи('-)"
            )
            raise UnprocessableEntityExceptionError(msg)
        return value

    @ninja_schema.model_validator("last_name")
    def clean_last_name(cls, value) -> str:
        """Helps to validate field last_name
        :param value: last_name
        :return: last_name
        """
        if not cls.validate_fio(value):
            msg = _(
                "Прізвище повинно починатися з великої літери"
                "(наступні маленькі), доступна кирилиця та латиниця, "
                "доступні спецсимволи('-)"
            )
            raise UnprocessableEntityExceptionError(msg)
        return value


class UserRegisterSchema(UserInBaseSchema):
    """Pydantic schema for User.

    Purpose of this schema to get user's
    personal data for registration
    """

    password1: SecretStr
    password2: SecretStr

    @staticmethod
    def check_password(password: str) -> None:
        """Helps to validate field password
        :param password: password
        :return: None
        """
        password_pattern = (
            "^(?=.*?[A-Z])(?=.*?[a-z])" "(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        )
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

    @ninja_schema.model_validator("password1")
    def clean_password1(cls, password1: SecretStr) -> SecretStr:
        """Helps to validate field password1
        :param password1: password1
        :return: password1
        """
        password = password1.get_secret_value()
        cls.check_password(password)
        return password1

    @ninja_schema.model_validator("password2")
    def clean_password2(cls, password2: SecretStr) -> SecretStr:
        """Helps to validate field password2
        :param password2: password2
        :return: password2
        """
        password = password2.get_secret_value()
        cls.check_password(password)
        return password2


class UserUpdateSchema(UserInBaseSchema):
    """Pydantic schema for update User.

    Purpose of this schema to get user's
    personal data for updating
    """

    birthday: str = None
    password: SecretStr = None

    @staticmethod
    def check_password(password: str) -> None:
        """Helps to validate field password
        :param password: password
        :return: None
        """
        password_pattern = (
            "^(?=.*?[A-Z])(?=.*?[a-z])" "(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        )
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

    @ninja_schema.model_validator("password")
    def clean_password(cls, password: SecretStr) -> SecretStr:
        """Helps to validate field password
        :param password: password
        :return: password
        """
        value = password.get_secret_value()
        cls.check_password(value)
        return password

    class Config(UserInBaseSchema.Config):
        optional = "__all__"


class UserOutSchema(ModelSchema):
    """Pydantic schema for User.

    Purpose of this schema to return user's
    personal data
    """

    city_display: str
    date_joined: str
    birthday: str

    @staticmethod
    def resolve_city_display(obj: User) -> str:
        """Makes city ready for rendering to frontend
        :param obj: User
        :return: city display format
        """
        return _(obj.get_city_display())

    @staticmethod
    def resolve_phone_number(obj: User) -> str:
        """Makes phone_number ready for rendering to frontend
        :param obj: User
        :return: phone_number display format
        """
        return str(obj.phone_number)

    @staticmethod
    def resolve_date_joined(obj: User) -> str:
        """Makes date_joined ready for rendering to frontend
        :param obj: User
        :return: date_joined display format
        """
        dj = obj.date_joined.strftime("%d.%m.%Y")
        return dj

    @staticmethod
    def resolve_birthday(obj: User) -> str:
        """Makes birthday ready for rendering to frontend
        :param obj: User
        :return: birthday display format
        """
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
            "birthday",
        ]
