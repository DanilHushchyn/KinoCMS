# Create your views here.

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import File
from ninja import Header
from ninja.files import UploadedFile
from ninja_extra import http_delete
from ninja_extra import http_get
from ninja_extra import http_post
from ninja_extra.controllers.base import ControllerBase
from ninja_extra.controllers.base import api_controller
from ninja_extra.permissions import IsAdminUser

from src.core.errors import InvalidTokenExceptionError
from src.core.errors import NotFoundExceptionError
from src.core.errors import UnprocessableEntityExceptionError
from src.core.schemas.base import LangEnum
from src.core.schemas.base import MessageOutSchema
from src.core.schemas.base import errors_to_docs
from src.core.utils import CustomJWTAuth
from src.mailing.errors import MailingIsActiveExceptionError
from src.mailing.models import MailTemplate
from src.mailing.schemas import MailingInSchema
from src.mailing.schemas import MailTemplateOutSchema
from src.mailing.schemas import TaskInfoOutSchema
from src.mailing.services.mailing import MailingService
from src.users.services.user_service import UserService


@api_controller(
    "/mailing", tags=["mailing"], permissions=[IsAdminUser()], auth=CustomJWTAuth()
)
class MailingController(ControllerBase):
    """A controller class for mailing.

    This class provides endpoints for
    get, post, create templates in the site
    for mailing
    """

    def __init__(self, user_service: UserService, mailing_service: MailingService):
        """Use this method to inject "services" to MailingController.

        :param user_service: variable for managing access control system
        """
        self.user_service = user_service
        self.mailing_service = mailing_service

    @http_post(
        "/template/",
        response=MailTemplateOutSchema,
        openapi_extra={
            "operationId": "create_template",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def create_template(
        self,
        request: HttpRequest,
        file: UploadedFile = File(...),
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MailTemplate:
        """Create template for mailing.

        Please provide:
          - **file**  file for new template

        Returns
        -------
          - **200**: Success response with the data.
          - **422**: Error: Unprocessable Entity.
            Причини: \n
                1) Дозволено відправляти тільки html \n
                2) Максимально дозволений розмір файлу 1MB \n
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.mailing_service.create_template(file)
        return result

    @http_get(
        "/templates/",
        response=list[MailTemplateOutSchema],
        openapi_extra={
            "operationId": "get_templates",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def get_templates(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> QuerySet:
        """Get last 5 templates for mailing.

        Returns
        -------
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
            "responses": errors_to_docs(
                {
                    400: [MailingIsActiveExceptionError()],
                    401: [InvalidTokenExceptionError()],
                    404: [NotFoundExceptionError(cls_model=MailTemplate)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def delete_template(
        self,
        request: HttpRequest,
        temp_id: int,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Delete template for mailing by id.

        Returns
        -------
          - **200**: Success response with the data.
          - **400**: Error: Not Found.\n
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
            "responses": errors_to_docs(
                {
                    400: [MailingIsActiveExceptionError()],
                    401: [InvalidTokenExceptionError()],
                    404: [NotFoundExceptionError(cls_model=MailTemplate)],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def start_mailing(
        self,
        request: HttpRequest,
        body: MailingInSchema,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> MessageOutSchema:
        """Start mailing letter to recipients.

        Returns
        -------
          - **200**: Success response with the data.
          - **400**: Error: Not Found. \n
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
        response={
            200: TaskInfoOutSchema,
            201: MessageOutSchema,
            202: MessageOutSchema,
        },
        summary="Get status of mailing (Long polling)",
        openapi_extra={
            "operationId": "status_mailing",
            "responses": errors_to_docs(
                {
                    401: [InvalidTokenExceptionError()],
                    422: [UnprocessableEntityExceptionError()],
                }
            ),
        },
    )
    def status_mailing(
        self,
        request: HttpRequest,
        accept_lang: LangEnum = Header(alias="Accept-Language", default="uk"),
    ) -> dict:
        """Get status for current mailing.

        Returns
        -------
          - **200**: Повертається прогресс розсилання.
          - **201**: Розсилання успішно виконане.
          - **202**: Hа теперішній час розсилання не активне.
          - **404**: Error: Not Found. \n
            Причини: \n
                1) Не знайдено: немає збігів шаблонів
                   на заданному запиті.
          - **422**: Error: Unprocessable Entity.
          - **500**: Internal server error if an unexpected error occurs.

        """
        result = self.mailing_service.get_task_info()
        return result
