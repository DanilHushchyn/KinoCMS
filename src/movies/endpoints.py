"""Endpoints for movie"""

from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest
from django_countries.data import COUNTRIES
from ninja import Header
from ninja_extra import http_delete
from ninja_extra import http_get
from ninja_extra import http_patch
from ninja_extra import http_post
from ninja_extra.controllers.base import ControllerBase
from ninja_extra.controllers.base import api_controller
from ninja_extra.pagination.decorator import paginate
from ninja_extra.permissions import IsAdminUser
from ninja_extra.schemas.response import PaginatedResponseSchema

from src.core.errors import InvalidTokenExceptionError
from src.core.errors import NotFoundExceptionError
from src.core.errors import NotUniqueFieldExceptionError
from src.core.errors import UnprocessableEntityExceptionError
from src.core.models import Image
from src.core.schemas.base import LangEnum
from src.core.schemas.base import MessageOutSchema
from src.core.schemas.base import errors_to_docs
from src.core.utils import CustomJWTAuth
from src.movies.models import Movie
from src.movies.models import MovieParticipant
from src.movies.models import Tech
from src.movies.schemas import MovieCardOutSchema
from src.movies.schemas import MovieClientOutSchema
from src.movies.schemas import MovieInSchema
from src.movies.schemas import MovieOutSchema
from src.movies.schemas import MovieParticipantOutSchema
from src.movies.schemas import MovieParticipantRoleOutSchema
from src.movies.schemas import MovieScheduleFilterSchema
from src.movies.schemas import MovieSearchOutSchema
from src.movies.schemas import MovieUpdateSchema
from src.movies.schemas import ReleaseEnum
from src.movies.schemas import TechOutSchema
from src.movies.service import MovieService


@api_controller("/movie", tags=["movies"])
class MovieController(ControllerBase):
    """A controller class for managing movie in system.

    This class provides endpoints for
    get, post, update, delete movie in the site
    """

    def __init__(self, movie_service: MovieService):
        """Use this method to inject "services" to MovieController.

        :param movie_service: variable for managing movies
        """
        self.movie_service = movie_service

    @http_get(
        "/legal-ages/",
        response=PaginatedResponseSchema[list],
        openapi_extra={
            "operationId": "get_movie_legal_ages",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_movie_legal_ages(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> list:
        """Get movie legal ages for input.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.get_legal_ages()
        return result

    @http_get(
        "/genres/",
        response=PaginatedResponseSchema[list],
        openapi_extra={
            "operationId": "get_movie_genres",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_movie_genres(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> list:
        """Get genres for input.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.get_genres()
        return result

    @http_get(
        "/techs/",
        response=PaginatedResponseSchema[TechOutSchema],
        openapi_extra={
            "operationId": "get_techs",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_techs(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet[Tech]:
        """Get techs for input.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.get_techs()
        return result

    @http_get(
        "/countries/",
        response=PaginatedResponseSchema[list],
        openapi_extra={
            "operationId": "get_countries",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_countries(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> list[tuple[str, Any]]:
        """Get countries for input.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        return list(COUNTRIES.items())

    @http_get(
        "/participants/",
        response=PaginatedResponseSchema[MovieParticipantOutSchema],
        openapi_extra={
            "operationId": "get_participants",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_participants(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet:
        """Get participants for input.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.get_participants()
        return result

    @http_get(
        "/participants-grouped/",
        response=list[MovieParticipantRoleOutSchema],
        openapi_extra={
            "operationId": "get_participants_grouped",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_participants_grouped(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet:
        """Get participants for input.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.get_participants_grouped()
        return result

    @http_get(
        "/all-cards/",
        response=PaginatedResponseSchema[MovieCardOutSchema],
        openapi_extra={
            "operationId": "get_all_movie_cards",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_all_movie_cards(
        self,
        request: HttpRequest,
        release: ReleaseEnum = ReleaseEnum.Current,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet:
        """Get all movie cards.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.get_all(release=release.value)
        return result

    @http_post(
        "/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "create_movie",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    404: [
                        NotFoundExceptionError(cls_model=Movie),
                        NotFoundExceptionError(
                            cls_model=MovieParticipant, field="participants"
                        ),
                        NotFoundExceptionError(cls_model=Tech, field="techs"),
                    ],
                    409: [NotUniqueFieldExceptionError(field="name")],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def create_movie(
        self,
        request: HttpRequest,
        body: MovieInSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Create movie.

        Please provide:
          - **body**  body for creating new movie

        Returns
        -------
          - **200**: Success response with the data.
          - **409**: Error: Conflict.
            Причини: \n
                1) Поле name повинно бути унікальним. Ця назва вже зайнята
          - **422**: Error: Unprocessable Entity. \n
            Причини: \n
                1) Максимальни довжина description 20_000 символів \n
                2) Максимальни довжина name 100 символів \n
                3) Максимальни довжина seo_title 60 символів \n
                4) Максимальни довжина seo_description 160 символів \n
          - **500**: Internal server error if an unexpected error occurs.

        Operations with gallery items:
         - Delete \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=true \n
         - Update \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=false \n
             3. Be sure to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
         - Create:
             1. Do not specify the id field \n
             3. Be sure to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
             4. Be sure to specify the field delete=false \n

        """
        result = self.movie_service.create(schema=body, request=request)
        return result

    @http_patch(
        "/{mv_slug}/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "update_movie",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    404: [
                        NotFoundExceptionError(cls_model=Movie),
                        NotFoundExceptionError(cls_model=Image),
                        NotFoundExceptionError(
                            cls_model=MovieParticipant, field="participants"
                        ),
                    ],
                    409: [NotUniqueFieldExceptionError(field="name")],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def update_movie(
        self,
        request: HttpRequest,
        mv_slug: str,
        body: MovieUpdateSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Update movie by slug.

        Please provide:
          - **body**  body for creating new movie

        Returns
        -------
          - **200**: Success response with the data.
          - **404**: Error: Not Found. \n
            Причини: \n
                1) Не знайдено: немає збігів фільмів
                   на заданному запиті. \n
          - **409**: Error: Conflict. \n
            Причини: \n
                1) Поле name повинно бути унікальним. Ця назва вже зайнята
          - **422**: Error: Unprocessable Entity. \n
            Причини: \n
                1) Максимальни довжина description 20_000 символів \n
                2) Максимальни довжина name 100 символів \n
                3) Максимальни довжина seo_title 60 символів \n
                4) Максимальни довжина seo_description 160 символів \n
          - **500**: Internal server error if an unexpected error occurs.

        Operations with gallery items:
         - Delete \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=true \n
         - Update \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=false \n
             3. Be sure to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
         - Create:
             1. Do not specify the id field \n
             3. Be sure to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
             4. Be sure to specify the field delete=false \n

        """
        result = self.movie_service.update(
            mv_slug=mv_slug, schema=body, request=request
        )
        return result

    @http_get(
        "/{mv_slug}/",
        response=MovieOutSchema,
        openapi_extra={
            "operationId": "get_movie_by_slug",
            "responses": errors_to_docs(
                {
                    404: [NotFoundExceptionError(cls_model=Movie)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_movie_by_slug(
        self,
        request: HttpRequest,
        mv_slug: str,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> Movie:
        """Get movie by slug.

        Please provide:
          - **mv_slug**  slug of movie

        Returns
        -------
          - **200**: Success response with the data.
          - **404**: Error: Not Found. \n
            Причини: \n
                1) Не знайдено: немає збігів фільмів
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.get_by_slug(mv_slug=mv_slug)
        return result

    @http_delete(
        "/{mv_slug}/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "delete_movie_by_slug",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    404: [NotFoundExceptionError(cls_model=Movie)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def delete_movie_by_slug(
        self,
        request: HttpRequest,
        mv_slug: str,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Delete movie by slug.

        Please provide:
          - **mv_slug**  slug of movie

        Returns
        -------
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів фільмів
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.delete_by_slug(mv_slug=mv_slug)
        return result


@api_controller("/movie", tags=["movies"])
class MovieClientController(ControllerBase):
    """A controller class for managing movie in client site.

    This class provides endpoints for
    get, movie in the site
    """

    def __init__(self, movie_service: MovieService):
        """Use this method to inject "services" to MovieClientController.

        :param movie_service: variable for managing movies
        """
        self.movie_service = movie_service

    @http_get(
        "/schedule-filter/",
        response=PaginatedResponseSchema[MovieScheduleFilterSchema],
        openapi_extra={
            "operationId": "get_movie_schedule_filter",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_movie_schedule_filter(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet[Movie]:
        """Get all movie cards.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.get_schedule_filter()
        return result

    get_techs = MovieController.get_techs

    get_all_movie_cards = MovieController.get_all_movie_cards

    @http_get(
        "/search/",
        response=PaginatedResponseSchema[MovieSearchOutSchema],
        openapi_extra={
            "operationId": "search_movies",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def search_movies(
        self,
        request: HttpRequest,
        search_line: str,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet[Movie]:
        """Search movies by search line.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.search(search_line)
        return result

    @http_get(
        "/seances-today-cards/",
        response=PaginatedResponseSchema[MovieCardOutSchema],
        openapi_extra={
            "operationId": "get_movie_today_cards",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_movie_today_cards(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet[Movie]:
        """Search movies by search line.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.get_today_movies()
        return result

    get_movie_by_slug = MovieController.get_movie_by_slug

    @http_get(
        "/{mv_slug}/",
        response=MovieClientOutSchema,
        openapi_extra={
            "operationId": "get_movie_by_slug",
            "responses": errors_to_docs(
                {
                    404: [NotFoundExceptionError(cls_model=Movie)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_movie_by_slug(
        self,
        request: HttpRequest,
        mv_slug: str,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> Movie:
        """Get movie by slug.

        Please provide:
          - **mv_slug**  slug of movie

        Returns
        -------
          - **200**: Success response with the data.
          - **404**: Error: Forbidden. \n
            Причини: \n
                1) Не знайдено: немає збігів фільмів
                   на заданному запиті. \n
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.movie_service.get_by_slug(mv_slug=mv_slug)
        return result
