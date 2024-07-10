# Create your views here.
from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_extra.permissions.common import IsAdminUser

from src.core.errors import UnprocessableEntityExceptionError
from src.core.schemas.base import LangEnum, errors_to_docs
from ninja_extra import http_get
from ninja import Header

from src.core.services.statistic import StatisticService
from src.core.utils import CustomJWTAuth


@api_controller("/statistic", tags=["statistic"],
                permissions=[IsAdminUser()],
                auth=CustomJWTAuth(), )
class StatisticController(ControllerBase):
    """
    A controller class for managing statistic in system.

    This class provides endpoints for
    get statistic in the site
    """

    def __init__(self, statistic_service: StatisticService):
        """
        Use this method to inject "services" to ImageController.

        :param statistic_service: variable for getting statistic
        """
        self.statistic_service = statistic_service

    @http_get(
        "/computed_nums/",
        response=dict,
        openapi_extra={
            "operationId": "get_computed_nums",

            "responses": errors_to_docs({
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def get_computed_nums(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> dict:
        """
        Get computed numbers of statistic for our site.

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.statistic_service.get_computed_nums()
        return result

    @http_get(
        "/most-popular-movies/",
        response=dict,
        openapi_extra={
            "operationId": "get_most_popular_movies",

            "responses": errors_to_docs({
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def get_most_popular_movies(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> dict:
        """
        Get get most popular movies on site.

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.statistic_service.get_most_popular_movies()
        return result

    @http_get(
        "/most-income-movies/",
        response=dict,
        openapi_extra={
            "operationId": "get_most_income_movies",

            "responses": errors_to_docs({
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def get_most_income_movies(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> dict:
        """
        Get most income movies on site.

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.statistic_service.get_most_income_movies()
        return result

    @http_get(
        "/most-popular-techs/",
        response=dict,
        openapi_extra={
            "operationId": "get_most_popular_techs",

            "responses": errors_to_docs({
                422: [
                    UnprocessableEntityExceptionError()
                ],
            }),
        },
    )
    def get_most_popular_techs(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> dict:
        """
        Get most popular techs on site.

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.statistic_service.get_most_popular_techs()
        return result
