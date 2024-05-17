# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.backends import ModelBackend

from src.users.models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, username=None,
                     password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
