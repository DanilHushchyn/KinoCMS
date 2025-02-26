"""Banners sliders essences endpoints"""

from django.http import HttpRequest
from ninja import Header
from ninja_extra import http_get
from ninja_extra import http_patch
from ninja_extra.controllers.base import ControllerBase
from ninja_extra.controllers.base import api_controller
from ninja_extra.pagination.decorator import paginate
from ninja_extra.permissions import IsAdminUser
from ninja_extra.schemas.response import PaginatedResponseSchema

from src.core.errors import InvalidTokenExceptionError
from src.core.errors import NotFoundExceptionError
from src.core.errors import UnprocessableEntityExceptionError
from src.core.schemas.base import LangEnum
from src.core.schemas.base import MessageOutSchema
from src.core.schemas.base import errors_to_docs
from src.core.utils import CustomJWTAuth
from src.pages.models import BottomSlider
from src.pages.models import BottomSliderItem
from src.pages.models import ETEndBBanner
from src.pages.models import TopSlider
from src.pages.models import TopSliderItem
from src.pages.schemas.banners_sliders import BottomSliderOutSchema, TopSliderClientOutSchema
from src.pages.schemas.banners_sliders import BottomSliderUpdateSchema
from src.pages.schemas.banners_sliders import ETEndBBannerOutSchema
from src.pages.schemas.banners_sliders import ETEndBBannerUpdateSchema
from src.pages.schemas.banners_sliders import TopSliderOutSchema
from src.pages.schemas.banners_sliders import TopSliderUpdateSchema
from src.pages.services.banners_sliders import SliderService


@api_controller("/slider", tags=["sliders"])
class SliderController(ControllerBase):
    """A controller class for managing slider in admin site.

    This class provides endpoints for
    get, update, delete slider in the admin site
    """

    def __init__(self, slider_service: SliderService):
        """Use this method to inject "services" to SliderController.

        :param slider_service: variable for managing sliders
        """
        self.slider_service = slider_service

    @http_get(
        "/speed-choices/",
        response=PaginatedResponseSchema[list],
        openapi_extra={
            "operationId": "get_speed_choices",
            "responses": errors_to_docs(
                {
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    @paginate()
    def get_speed_choices(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> list:
        """Get speed choices for input.

        Returns
        -------
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
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    404: [
                        NotFoundExceptionError(cls_model=TopSlider),
                        NotFoundExceptionError(cls_model=TopSliderItem),
                    ],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def update_top_slider(
        self,
        request: HttpRequest,
        body: TopSliderUpdateSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Update top slider and it's items.

        Please provide:
          - **body**  body for updating related items to top slider

        Returns
        -------
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity. \n
          - **500**: Internal server error if an unexpected error occurs.

        Operations with slider items:
         - Delete \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=true \n
         - Update \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=false \n
             3. It is optional to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
             4. It is not necessary to specify the url field
             5. It is not necessary to specify the text_uk, text_ru field
         - Create:
             1. Do not specify the id field \n
             2. Be sure to specify the url field \n
             3. Be sure to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
             4. Be sure to specify the field delete=false \n
             5. Be sure to specify the text_uk, text_ru field

        """
        result = self.slider_service.update_top_slider(schema=body)
        return result

    @http_get(
        "/top/",
        response=TopSliderOutSchema,
        openapi_extra={
            "operationId": "get_top_slider",
            "responses": errors_to_docs(
                {
                    404: [
                        NotFoundExceptionError(cls_model=TopSlider),
                    ],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_top_slider(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> TopSlider:
        """Get top slider and related items for admin.

        Returns
        -------
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
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    404: [
                        NotFoundExceptionError(cls_model=BottomSlider),
                        NotFoundExceptionError(cls_model=BottomSliderItem),
                    ],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def update_bottom_slider(
        self,
        request: HttpRequest,
        body: BottomSliderUpdateSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Update bottom slider and it's items.

        Please provide:
          - **body**  body for updating related items to bottom slider

        Returns
        -------
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity. \n
          - **500**: Internal server error if an unexpected error occurs.

        Operations with slider items:
         - Delete \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=true \n
         - Update \n
             1. Be sure to specify the id field \n
             2. Be sure to specify the field delete=false \n
             3. It is optional to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
             4. It is not necessary to specify the url field
         - Create:
             1. Do not specify the id field \n
             2. Be sure to specify the url field \n
             3. Be sure to specify the image field \n
                 a) required image if filename is specified. Format base64(svg,png,jpg,jpeg,webp) \n
                 b) filename is required if image is specified. Example: *filename.png* \n
                 c) optional alt. If you don't specify it, I'll take the value from filename \n
             4. Be sure to specify the field delete=false \n

        """
        result = self.slider_service.update_bottom_slider(schema=body)
        return result

    @http_get(
        "/bottom/",
        response=BottomSliderOutSchema,
        openapi_extra={
            "operationId": "get_bottom_slider",
            "responses": errors_to_docs(
                {
                    404: [NotFoundExceptionError(cls_model=BottomSlider)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_bottom_slider(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> BottomSlider:
        """Get bottom slider and related items for admin.

        Returns
        -------
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
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    404: [NotFoundExceptionError(cls_model=ETEndBBanner)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def update_etend_banner(
        self,
        request: HttpRequest,
        body: ETEndBBannerUpdateSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Update etend_banner and it's items.

        Please provide:
          - **body**  body for updating related items to etend_banner

        Returns
        -------
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
            "responses": errors_to_docs(
                {
                    404: [NotFoundExceptionError(cls_model=ETEndBBanner)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_etend_banner(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> ETEndBBanner:
        """Get get_etend_banner and related items for admin.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.slider_service.get_etend_banner()
        return result


@api_controller("/slider", tags=["sliders"])
class SliderClientController(ControllerBase):
    """A controller class for managing slider in client site.

    This class provides endpoints for
    get,  slider in the client site
    """

    def __init__(self, slider_service: SliderService):
        """Use this method to inject "services" to SliderClientController.

        :param slider_service: variable for managing sliders
        """
        self.slider_service = slider_service

    @http_get(
        "/top/",
        response=TopSliderClientOutSchema,
        openapi_extra={
            "operationId": "get_top_slider",
            "responses": errors_to_docs(
                {
                    404: [
                        NotFoundExceptionError(cls_model=TopSlider),
                    ],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_top_slider(
            self,
            request: HttpRequest,
            accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> TopSlider:
        """Get top slider and related items for admin.

        Returns
        -------
          - **200**: Success response with the data.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.slider_service.get_top_slider()
        return result
    get_bottom_slider = SliderController.get_bottom_slider
    get_etend_banner = SliderController.get_etend_banner
