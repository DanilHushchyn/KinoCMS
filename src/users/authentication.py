"""Rewrite authentication for project"""

from django.contrib.auth.backends import ModelBackend

from src.users.models import User


class EmailBackend(ModelBackend):
    """Class implements email prefered authentication instead username"""

    def authenticate(self, request, email=None, username=None, password=None, **kwargs):
        """Method for rewriting auth to email based instead username
        :param request: request
        :param email: email
        :param username: username
        :param password: password
        :param kwargs: kwargs
        :return: User() or None
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
