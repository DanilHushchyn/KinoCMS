import jwt
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from os.path import splitext
from django.shortcuts import get_object_or_404
from jwt.exceptions import PyJWTError
from ninja.errors import HttpError

from ninja_extra import permissions

from config.settings import settings


def get_current_user(token: str):
    """
    Check auth user.

    """
    try:
        code, token = token.split(" ")
        if code != "Bearer":
            raise ValueError
        payload = jwt.decode(token, settings.NINJA_JWT["SIGNING_KEY"], algorithms=[settings.NINJA_JWT["ALGORITHM"]])
    except (PyJWTError, ValueError):
        return None

    token_exp = datetime.fromtimestamp(int(payload["exp"]))
    if token_exp < datetime.utcnow():
        return None

    user = get_object_or_404(get_user_model(), id=payload["user_id"])
    return user


# class AdminOnly(permissions.BasePermission):
#     def has_permission(self, request, controller):
#         print(request.user.id)
#         print(111)
#         controller.
#
#         # token = request.headers
#         # user = get_current_user(token)
#         # print(user)
#         return request.auth.ggg
