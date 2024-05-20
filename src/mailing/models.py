from django.db import models

from src.core.utils import get_timestamp_path


# Create your models here.
class MailTemplate(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_timestamp_path, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
        verbose_name = "MailTemplate"
        verbose_name_plural = "MailTemplates"
        db_table = 'mail_templates'
