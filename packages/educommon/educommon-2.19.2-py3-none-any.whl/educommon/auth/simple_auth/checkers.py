# coding: utf-8
u"""Классы, осуществляющие проверку пользовательских данных."""
from __future__ import absolute_import

from m3_django_compat import get_user_model


MESSAGE_USER_NOT_EXISTS = u'Пользователь не найден.'
MESSAGE_PASSWORD_INCORRECT = u'Неверный логин или пароль.'
MESSAGE_USER_INACTIVE = u'Пользователь заблокирован'


User = get_user_model()


class DefaultLoginChecker(object):

    u"""Проверяет данные при входе."""

    def _check_lic(self, *args, **kwargs):
        # TODO: проверка лицензии
        request = kwargs['request']
        return None

    def _check_user_exists(self, *args, **kwargs):
        u"""Проверка существования пользователя с таким username."""
        username = kwargs['username']
        if not User.objects.filter(username=username).exists():
            return MESSAGE_USER_NOT_EXISTS

    def _check_user_active(self, *args, **kwargs):
        u"""Проверка что пользователь активен."""
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return MESSAGE_USER_NOT_EXISTS
        else:
            if not user.is_active:
                return MESSAGE_USER_INACTIVE

    def _check_user_password(self, *args, **kwargs):
        u"""Проверка существования пользователя с таким username/password."""
        username = kwargs['username']
        password = kwargs['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return MESSAGE_USER_NOT_EXISTS
        else:
            if not user.check_password(password):
                return MESSAGE_PASSWORD_INCORRECT

    _checkers = [
        _check_lic,
        _check_user_exists,
        _check_user_active,
        _check_user_password,
    ]

    def check(self, request, username, password):
        u"""Выполняет проверки по цепочке до первой ошибки.

        Если ошибки не возникло, LoginAction производит аутентификацию
        средствами django.
        """
        for checker in self._checkers:
            error = checker(
                self, request=request, username=username, password=password)

            if error:
                return error
