from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveModelBackend(ModelBackend):
    """Отключение зависимости от регистра"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        usermodel = get_user_model()
        try:
            user = usermodel.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
            else:
                return None
        except usermodel.DoesNotExist:
            return None


class EmailBackend(ModelBackend):
    """Вход по email"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        usermodel = get_user_model()
        try:
            user = usermodel.objects.get(email=username)
        except usermodel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None