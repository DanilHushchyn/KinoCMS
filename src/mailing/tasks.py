"""Celery task for implementing mailing"""

from celery import current_task
from celery.app import shared_task
from django.core.mail import EmailMultiAlternatives

from config.settings import settings
from src.users.models import User


@shared_task()
def make_mailing(user_ids: list | None, html_content: str) -> str:
    """Send letter to user and ask him to confirm registration
    In letter he will find link which redirects him to the site
    for confirmation
    :param html_content: letter in html format
    :param user_ids: list of users for mailing
    """
    if user_ids is None:
        users = User.objects.only("email").all()
    else:
        users = User.objects.only("id", "email").filter(id__in=user_ids)

    recipients = [user.email for user in users]
    current_task.update_state(
        state="PROGRESS", meta={"current": 0, "total": len(recipients)}
    )
    for index, recipient in enumerate(recipients, start=1):
        email = EmailMultiAlternatives(
            "KinoCMS",
            "",
            settings.EMAIL_HOST_USER,
            [recipient],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)
        if index == len(recipients):
            current_task.update_state(
                state="COMPLETE", meta={"current": index, "total": len(recipients)}
            )
        else:
            current_task.update_state(
                state="PROGRESS", meta={"current": index, "total": len(recipients)}
            )

    return "COMPLETE"
