from typing import Any, Tuple, List

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase
from ninja_extra.pagination.decorator import paginate
from ninja_extra.schemas.response import PaginatedResponseSchema
from src.core.schemas.base import LangEnum, MessageOutSchema
from ninja_extra.permissions import IsAdminUser
from ninja_extra import http_get, http_post, http_patch, http_delete
from ninja import Header
from django.utils.translation import gettext as _

from src.core.utils import CustomJWTAuth
from src.pages.models import TopSlider, BottomSlider, ETEndBBanner
from src.pages.schemas import *
from src.pages.schemas.banners_sliders import TopSliderUpdateSchema, TopSliderOutSchema, BottomSliderOutSchema, \
    BottomSliderUpdateSchema, ETEndBBannerUpdateSchema, ETEndBBannerOutSchema
from src.pages.services.banners_sliders import SliderService


# from src.pages.services import SliderService


@api_controller("/slider", tags=["sliders"])
class SliderController(ControllerBase):
    """
    A controller class for managing slider in system.

    This class provides endpoints for
    get, update, delete slider in the admin panel
    """

    def __init__(self, slider_service: SliderService):
        """
        Use this method to inject "services" to SliderController.

        :param slider_service: variable for managing sliders
        """
        self.slider_service = slider_service

    @http_get(
        "/speed-choices/",
        response=PaginatedResponseSchema[List],
        openapi_extra={
            "operationId": "get_speed_choices",
            "responses": {
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error "
                                   "if an unexpected error occurs.",
                },
            },
        },
    )
    @paginate()
    def get_speed_choices(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> List:
        """
        Get speed choices for input.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.slider_service.get_speed_choices()
        return result

    @http_patch(
        "/top/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "update_top_slider",
            "responses": {
                403: {
                    "description": "Error: Forbidden",
                },
                404: {
                    "description": "Error: Not Found",
                },
                409: {
                    "description": "Error: Conflict",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error "
                                   "if an unexpected error occurs.",
                },
            },
        },
    )
    def update_top_slider(
            self,
            request: HttpRequest,
            body: TopSliderUpdateSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Update top slider and it's items.

        Please provide:
          - **body**  body for updating related items to top slider

        Returns:
          - **200**: Success response with the data.
          - **403**: Error: Forbidden. \n
            Причини: \n
                1) Недійсне значення (не написане великими літерами).
                   З великих літер повиннен починатися text \n
          - **422**: Error: Unprocessable Entity. \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.slider_service.update_top_slider(schema=body)
        return result

    @http_get(
        "/top/",
        response=TopSliderOutSchema,
        openapi_extra={
            "operationId": "get_top_slider",
            "responses": {
                404: {
                    "description": "Error: Not Found",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error "
                                   "if an unexpected error occurs.",
                },
            },
        },
    )
    def get_top_slider(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> TopSlider:
        """
        Get top slider and related items for admin.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.slider_service.get_top_slider()
        return result

    @http_patch(
        "/bottom/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "update_bottom_slider",
            "responses": {
                403: {
                    "description": "Error: Forbidden",
                },
                404: {
                    "description": "Error: Not Found",
                },
                409: {
                    "description": "Error: Conflict",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error "
                                   "if an unexpected error occurs.",
                },
            },
        },
    )
    def update_bottom_slider(
            self,
            request: HttpRequest,
            body: BottomSliderUpdateSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Update bottom slider and it's items.

        Please provide:
          - **body**  body for updating related items to bottom slider

        Returns:
          - **200**: Success response with the data.
          - **403**: Error: Forbidden. \n
          - **422**: Error: Unprocessable Entity. \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.slider_service.update_bottom_slider(schema=body)
        return result

    @http_get(
        "/bottom/",
        response=BottomSliderOutSchema,
        openapi_extra={
            "operationId": "get_bottom_slider",
            "responses": {
                404: {
                    "description": "Error: Not Found",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error "
                                   "if an unexpected error occurs.",
                },
            },
        },
    )
    def get_bottom_slider(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> BottomSlider:
        """
        Get bottom slider and related items for admin.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.slider_service.get_bottom_slider()
        return result

    @http_patch(
        "/etend-banner/",
        response=MessageOutSchema,
        permissions=[IsAdminUser()],
        auth=CustomJWTAuth(),
        openapi_extra={
            "operationId": "update_etend_banner",
            "responses": {
                403: {
                    "description": "Error: Forbidden",
                },
                404: {
                    "description": "Error: Not Found",
                },
                409: {
                    "description": "Error: Conflict",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error "
                                   "if an unexpected error occurs.",
                },
            },
        },
    )
    def update_etend_banner(
            self,
            request: HttpRequest,
            body: ETEndBBannerUpdateSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Update etend_banner and it's items.

        Please provide:
          - **body**  body for updating related items to etend_banner

        Returns:
          - **200**: Success response with the data.
          - **403**: Error: Forbidden. \n
            Причини:
            1) Невірний формат кольору було введено
          - **422**: Error: Unprocessable Entity. \n
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.slider_service.update_etend_banner(schema=body)
        return result

    @http_get(
        "/etend-banner/",
        response=ETEndBBannerOutSchema,
        openapi_extra={
            "operationId": "get_etend_banner",
            "responses": {
                404: {
                    "description": "Error: Not Found",
                },
                422: {
                    "description": "Error: Unprocessable Entity",
                },
                500: {
                    "description": "Internal server error "
                                   "if an unexpected error occurs.",
                },
            },
        },
    )
    def get_etend_banner(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> ETEndBBanner:
        """
        Get get_etend_banner and related items for admin.

        Returns:
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.slider_service.get_etend_banner()
        return result
