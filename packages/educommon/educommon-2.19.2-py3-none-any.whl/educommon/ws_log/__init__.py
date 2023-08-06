# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import abc

import six


class IConfig(six.with_metaclass(abc.ABCMeta, object)):

    """Класс интерфейс для конфигурации менеджера логгеров веб-сервисов."""

    @abc.abstractproperty
    def loggers(self):
        """Список логгеров Системы.

        :return: Кортеж из строк, содержащих полные наименования
            модулей (с наименованием пакета), содержащих класс логгера.
        :type: tuple of strings
        """


#: Конфигурация приложения ``ws_log``.
#:
#: Заполняется экземпляром класса :class:`ws_log.IConfig`, либо его
#: потомком, при инициализации проекта *до* инициализации приложения
#: ``ws_log``.
config = None
