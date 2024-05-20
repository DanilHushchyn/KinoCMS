# Create your views here.
from typing import Dict, Any, List

from django.db.models import QuerySet
from ninja import File
from ninja.files import UploadedFile
from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase

from src.core.schemas import MessageOutSchema, LangEnum
from src.mailing.models import MailTemplate
from src.mailing.schemas import MailTemplateOutSchema
from src.mailing.services.mailing_service import MailingService
from src.users.services.user_service import UserService
from ninja_extra.permissions import IsAdminUser
from ninja_jwt.authentication import JWTAuth
from ninja_extra import http_delete, http_get, http_patch, http_post
from ninja import Header


@api_controller("/mailing", tags=["mailing"],
                # permissions=[IsAdminUser()], auth=JWTAuth()
                )
class MailingController(ControllerBase):
    """
    A controller class for mailing.

    This class provides endpoints for
    get, post, create templates in the site
    for mailing
    """

    def __init__(self, user_service: UserService,
                 mailing_service: MailingService):
        """
        Use this method to inject "services" to MailingController.

        :param user_service: variable for managing access control system
        """
        self.user_service = user_service
        self.mailing_service = mailing_service

    @http_post(
        "/template/",
        response=MailTemplateOutSchema,
        openapi_extra={
            "responses": {
                403: {
                    "description": "Error: Forbidden",
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
    def create_template(
            self,
            request: HttpRequest,
            file: UploadedFile = File(...),
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MailTemplate:
        """
        Create template for mailing.

        Please provide:
          - **file**  file for new template

        Returns:
          - **200**: Success response with the data.
          - **403**: Error: Forbidden. \n
              Причини:
              1) Дозволено відправляти тільки html
              2) Максимально дозволений розмір файлу 1MB
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.mailing_service.create_template(file)
        return result

    @http_get(
        "/templates/",
        response=List[MailTemplateOutSchema],
        openapi_extra={
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
    def get_templates(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> QuerySet:
        """
        Get last 5 templates for mailing.

        Returns:
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.mailing_service.get_templates()
        return result

    @http_delete(
        "/template/{temp_id}/",
        response=MessageOutSchema,
        openapi_extra={
            "responses": {
                404: {
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
    def delete_template(
            self,
            request: HttpRequest,
            temp_id: int,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Delete template for mailing by id.

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Conflict.
              Причини:
              1) Не знайдено: немає збігів шаблонів
              на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.mailing_service.delete_template(temp_id=temp_id)
        return result

