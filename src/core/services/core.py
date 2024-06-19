from typing import Type

from django.db.models import Model, Q
from django.http import HttpRequest, HttpResponse
from ninja.errors import HttpError, ValidationError
from django.utils.translation import gettext as _
from ninja_extra.exceptions import ParseError, APIException
from src.core.exceptions import FieldNotUniqueError
from ninja_extra import status


class CoreService:
    """
    A service class for solving common task in our system.
    """

    @staticmethod
    def check_field_unique(request: HttpRequest,
                           field_name: str,
                           value: str,
                           model: Type[Model],
                           instance: Model = None) \
            -> HttpResponse:
        """
        Check field for unique in model;
        :param request: HttpRequest
        :param field_name: contain field name for unique checking;
        :param value contain field value for unique checking;
        :param model for checking for unique
        :param instance checks for unique if we have update request
        """
        if value is not None:
            instances = (model.objects
                         .filter(**{field_name: value}))
            if instances and instance:
                instances = instances.exclude(id=instance.id)
            if instances.count():
                msg = _(f'Поле повинно бути унікальним. '
                        f'*{value}* - Ця назва вже зайнята')
                raise FieldNotUniqueError(
                    detail={
                        "detail": msg,
                        "field": field_name,
                    })
