"""App for implementing common features"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Core app config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.core"
