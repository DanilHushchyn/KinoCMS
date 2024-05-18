# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "users".

implement logic for encoding and decoding data into python
object and json
"""
from typing import List, Any, Tuple

from ninja import ModelSchema, Schema
from pydantic.functional_validators import field_validator
from pydantic.networks import EmailStr
from datetime import date
from pydantic_extra_types.phone_numbers import PhoneNumber

from pydantic.types import SecretStr, constr
from src.users.models import User
from django.utils.translation import gettext as _


class UserRegisterSchema(ModelSchema):
    """
    Pydantic schema for User.

    Purpose of this schema to get user's
    personal data for registration
    """
    password1: SecretStr
    password2: SecretStr

    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "nickname",
                  "city",
                  "man",
                  "phone_number",
                  "email",
                  "address",
                  "birthday", ]


class UserUpdateSchema(ModelSchema):
    """
    Pydantic schema for update User.

    Purpose of this schema to get user's
    personal data for updating
    """

    # first_name: str = None
    # last_name: str = None
    # nickname: str = None
    # man: bool = None
    # phone_number: PhoneNumber = None
    # email: EmailStr = None
    # address: str = None
    # birthday: date = None
    city: str = None

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "nickname",
            "city",
            "man",
            "phone_number",
            "email",
            "address",
            "birthday", ]
        fields_optional = "__all__"

    @field_validator('city')
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        print('hello')
        # if ' ' not in v:
        #     raise ValueError('must contain a space')
        # return v.title()
class UserOutSchema(ModelSchema):
    """
    Pydantic schema for User.

    Purpose of this schema to return user's
    personal data
    """
    city_display: str

    @staticmethod
    def resolve_phone_number(obj):
        return str(obj.phone_number)

    @staticmethod
    def resolve_city_display(obj: User):
        return _(obj.get_city_display())

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "nickname",
            "city",
            "man",
            "phone_number",
            "email",
            "address",
            "date_joined",
            "birthday", ]


class UsersAllSchema(Schema):
    """
    Pydantic schema for BestSellers.

    Purpose of this schema to return info about product
    which ordered be parameter bought_count
    """

    items: List[UserOutSchema]
    count: int
    next: bool
    previous: bool
