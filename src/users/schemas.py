# -*- coding: utf-8 -*-
"""
This module contains pydantic schemas for app "users".

implement logic for encoding and decoding data into python
object and json
"""
from typing import List

from ninja import ModelSchema, Schema
from pydantic.networks import EmailStr
from datetime import date
from pydantic_extra_types.phone_numbers import PhoneNumber

from pydantic.types import SecretStr, constr
from src.users.models import User


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
                  "man",
                  "phone_number",
                  "email",
                  "address",
                  "birthday", ]


class UserUpdateSchema(Schema):
    """
    Pydantic schema for User.

    Purpose of this schema to get user's
    personal data for registration
    """

    first_name: str = None
    last_name: str = None
    nickname: str = None
    man: bool = None
    phone_number: PhoneNumber = None
    email: EmailStr = None
    address: str = None
    birthday: date = None


class UserOutSchema(ModelSchema):
    """
    Pydantic schema for User.

    Purpose of this schema to return user's
    personal data
    """

    @staticmethod
    def resolve_phone_number(obj):
        return str(obj.phone_number)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "nickname",
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
