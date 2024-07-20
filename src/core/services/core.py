from django.db.models import Model
from django.utils.translation import gettext as _

from src.core.errors import NotUniqueFieldExceptionError


class CoreService:
    """A service class for solving common task in our system."""

    @staticmethod
    def check_field_unique(
        field_name: str, value: str, model: type[Model], instance: Model = None
    ) -> None:
        """Check field for unique in model;
        :param field_name: contain field name for unique checking;
        :param value contain field value for unique checking;
        :param model for checking for unique
        :param instance checks for unique if we have update request
        """
        if value is not None:
            instances = model.objects.filter(**{field_name: value})
            if instances and instance:
                instances = instances.exclude(id=instance.id)
            if instances.count():
                msg = _(
                    "Поле повинно бути унікальним. " "*{value}* - Ця назва вже зайнята"
                ).format(value=value)
                raise NotUniqueFieldExceptionError(message=msg, field=field_name)
