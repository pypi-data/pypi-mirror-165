# coding: utf-8
from __future__ import absolute_import

from abc import ABCMeta
from abc import abstractproperty

import six


class IConfig(six.with_metaclass(ABCMeta, object)):
    u"""Конфигурация управлением доступом на основе ролей.

    Позволяет ограничивать выбор классов, на которые может ссылаться
    :class:`~educommon.auth.rbac.models.UserRole` в атрибуте ``user``.
    """

    @abstractproperty
    def user_types(self):
        """Типы классов пользователей, которым назначаются роли.

        Отсутствие указывает на то, что ограничение по назначаемым ролям будет
        отключено.

        :rtype: set of django.db.models.Model or bool
        """


class DefaultConfig(IConfig):
    u"""Конфигурация без ограничения ролей пользователей."""

    user_types = False


# : Конфигурация управлением доступом.
rbac_config = DefaultConfig()
