from typing import List
from celery.app import shared_task
from celery import current_task
from django.core.mail import EmailMultiAlternatives
from config.settings import settings
from src.mailing.models import MailTemplate
from src.users.models import User
from django.core.cache import cache


@shared_task()
def make_mailing(users_list: List | None, temp_id: int) -> None:
    """
    Send letter to user and ask him to confirm registration
    In letter he will find link which redirects him to the site
    for confirmation
    :param users_list: list of users for mailing
    :param temp_id: mail template's id for mailing
    """

    if not users_list:
        users = User.objects.only('email').all()
    else:
        users = User.objects.only('id', 'email').filter(id__in=users_list)
    temp = MailTemplate.objects.get(id=temp_id)

    recipients = [user.email for user in users]
    with open(f'media/{temp.file}', 'r') as file:
        html_content = file.read()
    for index, recipient in enumerate(recipients):
        email = EmailMultiAlternatives('KinoCMS', '',
                                       settings.EMAIL_HOST_USER,
                                       [recipient])
        email.attach_alternative(html_content, 'text/html')
        email.send()
        current_task.update_state(state='PROGRESS',
                                  meta={'current': index,
                                        'total': len(recipients)})

    cache.delete(f'mailing_task')