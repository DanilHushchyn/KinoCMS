from typing import Type

from django.db.models import Model, Q
from ninja.errors import HttpError
from django.utils.translation import gettext as _


class CoreService:
    """
    A service class for solving common task in our system.
    """

    @staticmethod
    def check_name_unique(value: str, model: Type[Model],
                          instance: Model = None)\
            -> bool:
        """
        Check name for name in model unique.
        """
        if value is not None:
            instances = (model.objects
                         .filter(Q(name_uk=value) |
                                 Q(name_ru=value)))
            if instances and instance:
                instances = instances.exclude(id=instance.id)
            if instances.count():
                msg = _('Поле name повинно бути унікальним. '
                        'Ця назва вже зайнята')
                raise HttpError(409, msg)
            else:
                return True
