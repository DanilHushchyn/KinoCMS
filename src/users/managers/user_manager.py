import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from ninja.errors import HttpError
from django.utils.translation import gettext as _

from loguru import logger
from typing import TYPE_CHECKING, List, Optional

from src.core.schemas import MessageOutSchema

if TYPE_CHECKING:
    from src.users.schemas import UserRegisterSchema, UserUpdateSchema


# um1.User
class CustomUserManager(UserManager):
    """
    Custom user manager it's manager for making request to User model
    here is redefined some methods for saving
    user and superuser with email instead of username
    """

    def _create_user(self, email: str, password: str,
                     **extra_fields) -> object:
        """
        Create and save a user with the given username,
        email, and password.
        :rtype: User
        :param email: email for new user
        :param password: password for new user
        :param extra_fields: others extra
        :return: User model instance
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields) -> object:
        """
        Create and save a user with the given username,
        email, and password.
        :rtype: User
        :param email: email for new user
        :param password: password for new user
        :param extra_fields: others extra fields
        :return: User model instance
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str = None,
                         password: str = None,
                         **extra_fields) -> object:
        """
        Create and save a superuser with the given email,
        password and extra fields.
        :rtype: User
        :param email: email for new user
        :param password: password for new user
        :param extra_fields: others extra fields
        :return: User model instance
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_by_id(self, user_id: int):

        """
        Get user's model instance by id
        :param user_id:
        :rtype: User
        :return: User model instance
        """
        try:
            user = self.model.objects.get(id=user_id)
        except self.model.DoesNotExist:
            raise HttpError(404,
                            _("Не знайдено: немає збігів користувачів"
                              " на заданному запиті."))
        return user

    def delete_by_id(self, user_id: int) -> MessageOutSchema:

        """
        Update user's model instance by id
        :param user_id:
        :rtype: User
        :return: User model instance
        """
        try:
            user = self.model.objects.get(id=user_id)
            user.delete()
        except self.model.DoesNotExist:
            raise HttpError(404,
                            _("Не знайдено: немає збігів користувачів"
                              " на заданному запиті."))
        msg = _("Користувач успішно видалений")
        return MessageOutSchema(detail=msg)

    def update_by_id(self, user_id: int,
                     user_body: 'UserUpdateSchema'):

        """
        Delete user's model instance by id
        :param user_body: user's new personal data
        for update
        :param user_id: user's id for update
        :rtype: User
        :return: User model instance
        """
        try:
            user = self.model.objects.get(id=user_id)
        except self.model.DoesNotExist:
            raise HttpError(404,
                            _("Не знайдено: немає збігів користувачів"
                              " на заданному запиті."))
        for field, value in user_body.dict().items():
            if value is not None:
                setattr(user, field, value)
        user.save()
        return user

    def register(self, user_body: 'UserRegisterSchema') -> None:
        """
        Get user model instance by id
        :param user_body: user's personal data for registration
        :rtype: User
        :return: User model instance
        """
        pass1 = user_body.password1.get_secret_value()
        pass2 = user_body.password2.get_secret_value()
        if pass1 != pass2:
            raise HttpError(403, _("Паролі не співпадають"))

        if self.model.objects.filter(email=user_body.email).exists():
            msg = _("Ця електронна адреса вже використовується")
            raise HttpError(409, msg)

        self.model.objects.create(
            first_name=user_body.first_name,
            last_name=user_body.last_name,
            nickname=user_body.nickname,
            man=user_body.man,
            phone_number=user_body.phone_number,
            email=user_body.email,
            address=user_body.address,
            birthday=user_body.birthday,
            password=make_password(pass1),

        )
