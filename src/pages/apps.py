"""App page"""

from django.apps import AppConfig


class PagesConfig(AppConfig):
    """App page config class"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.pages"
