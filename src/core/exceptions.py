"""Exceptions schema."""

from django.utils.translation import gettext as _
from ninja_extra import status
from ninja_extra.exceptions import APIException


class FieldNotUniqueError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _(f'Поле повинно бути унікальним. '
                       f'Ця назва вже зайнята')
    field = 'field'
