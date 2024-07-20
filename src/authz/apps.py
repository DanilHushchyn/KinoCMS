"""App for implementing authentication and authorization"""

from django.apps import AppConfig


class AuthzConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.authz"
