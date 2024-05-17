# -*- coding: utf-8 -*-
"""
In this module described all celery task for implementing
asynchronous logic in application users
"""
# from celery.app import shared_task
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from config import settings
from src.users.models import PasswordResetToken, User

#
# @shared_task
# def email_verification(user_id: int, token) -> dict:
#     """
#     Send letter to user and ask him to confirm registration
#     In letter he will find link which redirects him to the site
#     for confirmation
#     :param token:
#     :param user_id: stores user id
#     """
#     user = User.objects.get(id=user_id)
#     # Send confirmation email
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#
#     confirmation_url = f"{settings.FRONTEND_URL}/confirm-email/{uid}/{token}"
#     send_mail(
#         "Confirm Your Email for site GoldBoost",
#         f"Click the link to confirm your email: {confirmation_url}",
#         settings.DEFAULT_FROM_EMAIL,
#         [user.email],
#         fail_silently=False,
#     )
#     return {"message": "Confirmation email sent"}
#
#
# @shared_task
# def reset_password_confirm(user_id: int, token):
#     """
#     Send letter to user and ask him to confirm reset password.
#     In the letter he will find link which redirects him to the site
#     where he can change his password
#     :param token:
#     :param user_id: stores user id
#     """
#     user = User.objects.get(id=user_id)
#
#     # Generating a password reset token
#     PasswordResetToken.objects.create(user=user, token=token)
#
#     # Create a password reset confirmation link
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     reset_url = f"{settings.FRONTEND_URL}/confirm-reset/{uid}/{token}"
#
#     # Send an email with a link to confirm your password reset
#     send_mail(
#         "Password reset",
#         f"Click the following link to reset your password: {reset_url}",
#         settings.DEFAULT_FROM_EMAIL,
#         [user.email],
#         fail_silently=False,
#     )
#     return {"message": "Reset password confirmation sent to email"}
