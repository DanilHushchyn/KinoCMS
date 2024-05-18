"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import HttpRequest, HttpResponse
from django.urls import path, include
from ninja_extra import NinjaExtraAPI, status
from django.conf.urls.static import static
from django.utils.translation import gettext as _
from ninja.errors import AuthenticationError, ValidationError

from config.settings import settings
from src.authz.endpoints import CustomTokenObtainPairController
from src.users.endpoints import UsersKinoController

kino_api = NinjaExtraAPI(title='Kino', description='KINO API')

kino_api.register_controllers(CustomTokenObtainPairController)
kino_api.register_controllers(UsersKinoController)


@kino_api.exception_handler(AuthenticationError)
def user_unauthorized(request, exc):
    return kino_api.create_response(
        request,
        {"message": _("Не авторизований")},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@kino_api.exception_handler(ValidationError)
def http_exceptions_handler(request: HttpRequest, exc: ValidationError) \
        -> HttpResponse:
    """
    Handle all Validation errors.
    """
    error_list = []
    for error in exc.errors:
        location = error["loc"][0]
        field_full = ".".join(map(str, error["loc"][1:])) if len(error["loc"]) > 1 else None
        message = _(error["msg"])
        error_list.append(
            {
                "location": location,
                "field": field_full,
                "message": message.capitalize(),
            }
        )

    return kino_api.create_response(
        request,
        data={
            "error": {"status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                      "details": error_list},
        },
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


urlpatterns = [
    path('api/', kino_api.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
