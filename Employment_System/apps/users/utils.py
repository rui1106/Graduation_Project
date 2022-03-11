import re

from django.contrib.auth.backends import ModelBackend

from apps.users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    :param token:
    :param user:
    :param request:
    :return:
    """

    return {
        "code": 0,
        "user_id": user.id,
        "username": user.username
    }


def get_user_by_account(account):
    try:
        if re.match('^1[3-9]\d{9}$', account):
            user = User.objects.get(phone=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user
