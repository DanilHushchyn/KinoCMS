from src.mailing.models import MailTemplate
from ninja import ModelSchema


class MailTemplateOutSchema(ModelSchema):
    """
    Pydantic schema for MailTemplate.

    Purpose of this schema to return mail template data
    """

    class Meta:
        model = MailTemplate
        fields = [
            "id",
            "name",
        ]
