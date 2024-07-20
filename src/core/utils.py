"""Common utils for all apps"""

from datetime import datetime
from os.path import splitext
from typing import Any

from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.db.models import Model
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext as _
from ninja.errors import HttpError
from ninja.security import HttpBearer
from ninja_jwt.authentication import JWTBaseAuthentication
from phonenumber_field.validators import validate_international_phonenumber
from pydantic_core._pydantic_core import Url
from pytils.translit import slugify

from src.core.errors import UnprocessableEntityExceptionError
from src.users.models import User


def get_timestamp_path(instance: object, filename) -> str:
    """Make unique naming of files in directory media.

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
    """Returns paginated queryset by pages of any Model in our project.

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
    """Custom class for jwt auth"""

    def authenticate(self, request: HttpRequest, token: str) -> Any:
        """Overridden method for making easier to auth in system
        by special password instead making token(available also)
        :param request:
        :param token:
        :return:
        """
        if token == "admin":
            user = User.objects.get(id=1)
            request.user = user
            return user
        return self.jwt_authenticate(request, token)


primitives = (bool, str, int, float, Url)


def check_phone_number(phone_number: str) -> None:
    """Method for validation phone number
    :param phone_number:
    :return:
    """
    try:
        validate_international_phonenumber(phone_number)
    except ValidationError:
        msg = _("Введено некоректний номер телефону.")
        raise UnprocessableEntityExceptionError(message=msg)


def make_slug(value: str, model: Model, instance: Model = None) -> str:
    """Method for making uniques slug for particular model instance
    :param value: value for slugify
    :param model: type of model for checking on unique in db
    :param instance: instance of model that needs slug
    :return:
    """
    slug = slugify(value)
    counter = 1
    while True:
        objs = model.objects.filter(slug=slug)
        if instance:
            objs = objs.exclude(id=instance.id)

        if objs.count() == 0:
            return slug

        slug = f"{slug}-{counter}"
        counter += 1
