# Create your views here.
import time
from typing import Dict, Any, List

from django.db.models import QuerySet
from ninja import File
from ninja.files import UploadedFile
from django.http import HttpRequest
from ninja_extra.controllers.base import api_controller, ControllerBase

from src.core.schemas.base import MessageOutSchema, LangEnum
from src.core.utils import CustomJWTAuth
from src.mailing.models import MailTemplate
from src.mailing.schemas import (MailTemplateOutSchema, MailingInSchema,
                                 TaskInfoOutSchema)
from src.mailing.services.mailing_service import MailingService
from src.users.services.user_service import UserService
from ninja_extra.permissions import IsAdminUser
from ninja_jwt.authentication import JWTAuth
from ninja_extra import http_delete, http_get, http_patch, http_post
from ninja import Header


@api_controller("/mailing", tags=["mailing"],
                permissions=[IsAdminUser()],
                auth=CustomJWTAuth())
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
            "operationId": "create_template",
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
            Причини: \n
                1) Дозволено відправляти тільки html \n
                2) Максимально дозволений розмір файлу 1MB \n
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.mailing_service.create_template(file)
        return result

    @http_get(
        "/templates/",
        response=List[MailTemplateOutSchema],
        openapi_extra={
            "operationId": "get_templates",

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
            "operationId": "delete_template",
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
          - **403**: Error: Not Found.\n
            Причини: \n
                1) Не можна видаляти шаблони поки йде розсилання.
          - **404**: Error: Not Found.\n
            Причини: \n
                1) Не знайдено: немає збігів шаблонів
                   на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.mailing_service.delete_template(temp_id=temp_id)
        return result

    @http_post(
        "/start/",
        response=MessageOutSchema,
        openapi_extra={
            "operationId": "start_mailing",
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
    def start_mailing(
            self,

            request: HttpRequest,
            body: MailingInSchema,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> MessageOutSchema:
        """
        Start mailing letter to recipients.

        Returns:
          - **200**: Success response with the data.
          - **404**: Error: Not Found. \n
            Причини: \n
                1) Треба зачекати поки закінчиться поточне розсилання.
          - **404**: Error: Not Found.\n
            Причини: \n
                1) Не знайдено: немає збігів шаблонів
                   на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.mailing_service.send_mail(body)
        return result

    @http_get(
        "/status/",
        response={200: TaskInfoOutSchema, 201: MessageOutSchema},
        openapi_extra={
            "operationId": "status_mailing",
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
    def status_mailing(
            self,
            request: HttpRequest,
            accept_lang: LangEnum =
            Header(alias="Accept-Language",
                   default="uk"),
    ) -> dict:
        """
        Get status for current mailing.

        Returns:
          - **200**: Success response with the data.
          - **201**: Success mailing completed.
          - **404**: Error: Not Found. \n
            Причини: \n
                1) Не знайдено: немає збігів шаблонів
                   на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.
        """
        result = self.mailing_service.get_task_info()
        return result
