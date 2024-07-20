"""Common utils for movie app"""

from django.db import models
from multiselectfield import MultiSelectField as MSField


class MultiSelectField(MSField):
    """Custom Implementation of MultiSelectField
    to achieve Django 5.0 compatibility

    See:
    https://github.com/goinnn/django-multiselectfield/issues/141#issuecomment-1911731471
    """

    def _get_flatchoices(self):
        """Some method for adapting MultiselectField to Django 5.0+
        :return:
        """
        flat_choices = super(models.CharField, self).flatchoices

        class MSFFlatchoices(list):
            # Used to trick django.contrib.admin.utils.display_for_field
            # into not treating the list of values as a
            # dictionary key (which errors out)
            def __bool__(self):
                return False

            __nonzero__ = __bool__

        return MSFFlatchoices(flat_choices)

    flatchoices = property(_get_flatchoices)
