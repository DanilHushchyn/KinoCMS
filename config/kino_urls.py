"""URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

Examples
--------
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

from django.conf.urls.static import static
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import include
from django.urls import path
from django.utils.translation import gettext as _
from ninja.errors import AuthenticationError
from ninja.errors import HttpError
from ninja.errors import ValidationError
from ninja_extra import NinjaExtraAPI
from ninja_extra import status
from ninja_jwt.exceptions import AuthenticationFailed
from ninja_jwt.exceptions import InvalidToken

from config.settings import settings
from src.authz.endpoints import CustomTokenObtainPairController
from src.booking.endpoints.seance import SeanceController
from src.booking.endpoints.ticket import TicketController
from src.cinemas.endpoints.cinema import CinemaClientController
from src.cinemas.endpoints.hall import HallClientController
from src.core.endpoints.gallery import GalleryController
from src.core.errors import AuthenticationExceptionError
from src.core.errors import InvalidTokenExceptionError
from src.movies.endpoints import MovieClientController
from src.pages.endpoints.banners_sliders import SliderClientController
from src.pages.endpoints.news_promo import NewsPromoClientController
from src.pages.endpoints.page import PageClientController

kino_api = NinjaExtraAPI(title="KinoCMS (client-site)", description="CLIENT API")
kino_api.register_controllers(CustomTokenObtainPairController)
kino_api.register_controllers(GalleryController)
kino_api.register_controllers(CinemaClientController)
kino_api.register_controllers(HallClientController)
kino_api.register_controllers(MovieClientController)
kino_api.register_controllers(SeanceController)
kino_api.register_controllers(TicketController)
kino_api.register_controllers(PageClientController)
kino_api.register_controllers(NewsPromoClientController)
kino_api.register_controllers(SeanceController)
kino_api.register_controllers(SliderClientController)


@kino_api.exception_handler(AuthenticationError)
@kino_api.exception_handler(AuthenticationFailed)
def authentication_handler(request, exc):
    """Method for intercepting the default
    AuthenticationError and AuthenticationFailed
    errors and overriding it for unification purposes
    :param request: object of request
    :param exc: handeled exc
    :return: unified error
    """
    msg = _("Не авторизований")
    if isinstance(exc, AuthenticationFailed):
        msg = exc.detail["detail"]
    return kino_api.create_response(
        request,
        data={
            "status": status.HTTP_401_UNAUTHORIZED,
            "error": AuthenticationExceptionError(message=msg).error_detail,
        },
        status=status.HTTP_401_UNAUTHORIZED,
    )


@kino_api.exception_handler(InvalidToken)
def invalid_token_handler(request, exc):
    """Method for intercepting the default;
    InvalidToken
    error and overriding it for unification purposes
    :param request: object of request
    :param exc: handeled exc
    :return: unified error
    """
    return kino_api.create_response(
        request,
        data={
            "status": status.HTTP_401_UNAUTHORIZED,
            "error": InvalidTokenExceptionError(
                message=exc.detail["detail"]
            ).error_detail,
        },
        status=status.HTTP_401_UNAUTHORIZED,
    )


@kino_api.exception_handler(ValidationError)
def http_exceptions_handler(request: HttpRequest, exc: ValidationError) -> HttpResponse:
    """Handle all Validation errors."""
    error_list = []
    for error in exc.errors:
        location = error["loc"][0]
        field_full = (
            ".".join(map(str, error["loc"][1:])) if len(error["loc"]) > 1 else None
        )
        message = _(error["msg"])
        error_list.append(
            {
                "location": location,
                "field": field_full,
                "message": message,
            }
        )

    return kino_api.create_response(
        request,
        data={
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "error": {"code": "UNPROCESSABLE_ENTITY", "details": error_list},
        },
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@kino_api.exception_handler(HttpError)
def common_exception_handler(request, exc):
    """Method for intercepting the default;
    HttpError
    error and overriding it for unification purposes
    :param request: object of request
    :param exc: handeled exc
    :return: unified error
    """
    return kino_api.create_response(
        request,
        data={
            "status": exc.status_code,
            "error": {
                "code": "COMMON_ERROR",
                "details": [
                    {
                        "location": "",
                        "field": "",
                        "message": exc.message,
                    }
                ],
            },
        },
        status=exc.status_code,
    )


urlpatterns = [
    path("api/", kino_api.urls),
]
if settings.DEBUG:
    settings.INSTALLED_APPS += ["requests_tracker"]
    settings.MIDDLEWARE += ["requests_tracker.middleware.requests_tracker_middleware"]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__requests_tracker__/", include("requests_tracker.urls"))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
