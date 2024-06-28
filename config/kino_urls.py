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
from ninja_jwt.exceptions import InvalidToken, AuthenticationFailed

from config.settings import settings
from src.authz.endpoints import CustomTokenObtainPairController
from src.booking.endpoints.seance import SeanceController
from src.cinemas.endpoints.cinema import CinemaClientController
from src.cinemas.endpoints.hall import HallClientController
from src.core.endpoints.gallery import GalleryController
from src.core.errors import AuthenticationExceptionError, InvalidTokenExceptionError
from src.movies.endpoints import MovieClientController
from src.pages.endpoints.page import PageClientController
from src.pages.endpoints.news_promo import NewsPromoClientController
from src.pages.endpoints.banners_sliders import SliderClientController

kino_api = NinjaExtraAPI(title='KinoCMS (client-site)', description='CLIENT API')
kino_api.register_controllers(CustomTokenObtainPairController)
kino_api.register_controllers(GalleryController)
kino_api.register_controllers(CinemaClientController)
kino_api.register_controllers(HallClientController)
kino_api.register_controllers(MovieClientController)
kino_api.register_controllers(SeanceController)
kino_api.register_controllers(PageClientController)
kino_api.register_controllers(NewsPromoClientController)
kino_api.register_controllers(SeanceController)
kino_api.register_controllers(SliderClientController)


@kino_api.exception_handler(AuthenticationFailed)
def authentication_failed_handler(request, exc):
    return kino_api.create_response(
        request,
        data={
            "status": status.HTTP_401_UNAUTHORIZED,
            "error": AuthenticationExceptionError(
                message=exc.detail['detail']
            ).error_detail,
        },
        status=status.HTTP_401_UNAUTHORIZED,
    )


@kino_api.exception_handler(InvalidToken)
def invalid_token_handler(request, exc):
    return kino_api.create_response(
        request,
        data={
            "status": status.HTTP_401_UNAUTHORIZED,
            "error": InvalidTokenExceptionError(
                message=exc.detail['detail']
            ).error_detail,
        },
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
                "field": field_full.split('.')[1],
                "message": message,
            }
        )

    return kino_api.create_response(
        request,
        data={
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "error": {"code": "UNPROCESSABLE_ENTITY",
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
    # urlpatterns += [
    #     path("__debug__/", include("debug_toolbar.urls")),
    # ]
