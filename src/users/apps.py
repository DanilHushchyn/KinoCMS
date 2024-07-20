"""Application configuration for the users Django app."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Application configuration for the users Django app.

    This class defines configuration settings for the users Django app.
    It provides metadata about the app, such as the app's verbose name and
    any default configurations. It can also include signals to be executed
    when the app is ready or when it is being shut down.

    Usage:
        To use this configuration class, ensure that it is set as the default
        AppConfig for the app in the app's __init__.py file:

        ```
        default_app_config = 'myapp.apps.MyAppConfig'
        ```

    For more information on AppConfigs, see the Django documentation:
    https://docs.djangoproject.com/en/stable/ref/applications/#configuring-applications
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.users"
