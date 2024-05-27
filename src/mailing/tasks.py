import smtplib
from email.mime.text import MIMEText
from typing import List
from celery.app import shared_task
from celery import current_task
from django.core.mail import EmailMultiAlternatives
from config.settings import settings
from src.mailing.models import MailTemplate
from src.users.models import User
from django.core.cache import cache
import loguru


@shared_task()
def make_mailing(user_ids: List | None, temp_id: int) -> str:
    """
    Send letter to user and ask him to confirm registration
    In letter he will find link which redirects him to the site
    for confirmation
    :param user_ids: list of users for mailing
    :param temp_id: mail template's id for mailing
    """

    if user_ids is None:
        users = User.objects.only('email').all()
    else:
        users = User.objects.only('id', 'email').filter(id__in=user_ids)
    temp = MailTemplate.objects.get(id=temp_id)

    recipients = [user.email for user in users]
    with open(f'media/{temp.file}', 'r') as file:
        html_content = file.read()
    for index, recipient in enumerate(recipients, start=1):

        email = EmailMultiAlternatives('KinoCMS', '',
                                       settings.EMAIL_HOST_USER,
                                       [recipient],
                                       )
        email.attach_alternative(html_content, 'text/html')
        email.send(fail_silently=True)
        if index == len(recipients):
            current_task.update_state(state='COMPLETE',
                                      meta={'current': index,
                                            'total': len(recipients)})
        else:
            current_task.update_state(state='PROGRESS',
                                      meta={'current': index,
                                            'total': len(recipients)})

    return 'COMPLETE'
