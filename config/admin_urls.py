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
from django.shortcuts import render
from django.urls import path, include
from django.views.generic import View
from imagekit.utils import get_cache
from ninja_extra import NinjaExtraAPI, status
from django.conf.urls.static import static
from django.utils.translation import gettext as _
from ninja.errors import ValidationError, AuthenticationError, HttpError

from config.settings import settings
from src.authz.endpoints import CustomTokenObtainPairController
from src.cinemas.endpoints.cinema import CinemaController
from src.cinemas.endpoints.hall import HallController
from src.core.endpoints.gallery import GalleryController
from src.core.endpoints.statistic import StatisticController
from src.core.errors import (AuthenticationExceptionError,
                             InvalidTokenExceptionError)
from src.mailing.endpoints import MailingController
from src.movies.endpoints import MovieController
from src.pages.endpoints.banners_sliders import SliderController
from src.pages.endpoints.news_promo import NewsPromoController
from src.pages.endpoints.page import PageController
from src.users.endpoints import UsersAdminController
from django.core.cache import cache
from ninja_jwt.exceptions import InvalidToken, AuthenticationFailed

cache.delete('mailing_task')
cache = get_cache()
cache.clear()
admin_api = NinjaExtraAPI(title='KinoCMS (admin-panel)',
                          description='ADMIN API')
admin_api.register_controllers(StatisticController)
admin_api.register_controllers(CustomTokenObtainPairController)
admin_api.register_controllers(UsersAdminController)
admin_api.register_controllers(MailingController)
admin_api.register_controllers(GalleryController)
admin_api.register_controllers(CinemaController)
admin_api.register_controllers(MovieController)
admin_api.register_controllers(HallController)
admin_api.register_controllers(SliderController)
admin_api.register_controllers(NewsPromoController)
admin_api.register_controllers(PageController)


@admin_api.exception_handler(AuthenticationError)
@admin_api.exception_handler(AuthenticationFailed)
def authentication_handler(request, exc):
    msg = _("Не авторизований")
    if isinstance(exc, AuthenticationFailed):
        msg = exc.detail['detail']
    return admin_api.create_response(
        request,
        data={
            "status": status.HTTP_401_UNAUTHORIZED,
            "error": AuthenticationExceptionError(
                message=msg
            ).error_detail,
        },
        status=status.HTTP_401_UNAUTHORIZED,
    )


@admin_api.exception_handler(InvalidToken)
def invalid_token_handler(request, exc):
    return admin_api.create_response(
        request,
        data={
            "status": status.HTTP_401_UNAUTHORIZED,
            "error": InvalidTokenExceptionError(
                message=exc.detail['detail']
            ).error_detail,
        },
        status=status.HTTP_401_UNAUTHORIZED,
    )


@admin_api.exception_handler(ValidationError)
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
                "message": message,
            }
        )

    return admin_api.create_response(
        request,
        data={
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "error": {"code": "UNPROCESSABLE_ENTITY",
                      "details": error_list},
        },
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@admin_api.exception_handler(HttpError)
def common_exception_handler(request, exc):
    return admin_api.create_response(
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
                ]
            }
        },
        status=exc.status_code,
    )


class StatisticView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, '../templates/statistic/base.html', context={})


urlpatterns = [
    path('api/', admin_api.urls),
    path('statistic/', StatisticView.as_view())
]
if settings.DEBUG:
    settings.INSTALLED_APPS += ["requests_tracker"]
    settings.MIDDLEWARE += \
        ["requests_tracker.middleware.requests_tracker_middleware"]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # urlpatterns += [
    #     path("__debug__/", include("debug_toolbar.urls")),
    # ]
    urlpatterns += [path("__requests_tracker__/",
                         include("requests_tracker.urls"))]
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
