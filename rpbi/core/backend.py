# -*- coding: utf-8 -*-

from django.contrib.auth.backends import ModelBackend
from core.models import BaseRBPIUser


class SettingsBackend(ModelBackend):
    """Класс аутетификации для RBPI Пользователей"""

    def authenticate(self, request, username=None, password=None):
        login_valid = (
                username in
                list(BaseRBPIUser.objects.values_list('username', flat=True)))
        if login_valid:
            try:
                user = BaseRBPIUser.objects.get(username=username)
                if user.is_admin and password == user.password:
                    return user
                else:
                    return user

            except BaseRBPIUser.DoesNotExist:
                raise BaseRBPIUser.DoesNotExist
        return None

    def get_user(self, user_id):
        try:
            return BaseRBPIUser.objects.get(pk=user_id)
        except BaseRBPIUser.DoesNotExist:
            return None
