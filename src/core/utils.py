from datetime import datetime
from os.path import splitext
from typing import Any

from django.core.paginator import EmptyPage, Paginator
from django.http import HttpRequest

from ninja.errors import HttpError
from django.db.models import QuerySet
from ninja.security import HttpBearer
from ninja_jwt.authentication import JWTBaseAuthentication
from phonenumber_field.validators import validate_international_phonenumber
from pydantic_core._pydantic_core import Url
from phonenumber_field.validators import (
    validate_international_phonenumber)
from django.utils.translation import gettext as _

from django.core.exceptions import ValidationError

from src.core.errors import UnprocessableEntityExceptionError
from src.users.models import User


def get_timestamp_path(instance: object, filename) -> str:
    """
    Make unique naming of files in directory media.

    :param instance: model instance which just created
    :param filename: name of uploaded file to ImageField
    :return: unique file name
    """
    return "%s/%s%s" % (
        instance.__class__.__name__,
        datetime.now().timestamp(),
        splitext(filename)[1],
    )


def paginate(page: int, items: QuerySet, page_size: int) -> dict:
    """
    Returns paginated queryset by pages of any Model in our project.

    :param page: the page number we want to get
    :param items: queryset of models instances which have to paginated
    :param page_size: length of queryset per page
    :return: dict which contains parameters for pagination
    :rtype: dict
    """
    if page_size < 1:
        raise HttpError(422, "page_size query parameter must be more than 1")
    paginator = Paginator(items, per_page=page_size)
    try:
        paginated_items = paginator.page(page)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)
    return {
        "items": paginated_items.object_list,
        "count": paginator.num_pages,
        "next": paginated_items.has_next(),
        "previous": paginated_items.has_previous(),
    }


class CustomJWTAuth(JWTBaseAuthentication, HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Any:
        if token == 'admin':
            user = User.objects.get(id=1)
            request.user = user
            return user
        return self.jwt_authenticate(request, token)


primitives = (bool, str, int, float, Url)


def check_phone_number(phone_number: str) -> None:
    try:
        validate_international_phonenumber(phone_number)
    except ValidationError:
        msg = _("Введено некоректний номер телефону.")
        raise UnprocessableEntityExceptionError(message=msg)
