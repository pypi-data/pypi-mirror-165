# coding: utf-8
u"""Конфигурация асинхронной сборки отчета."""
from __future__ import absolute_import

import abc

import six


class ConstructorConfig(six.with_metaclass(abc.ABCMeta, object)):

    u"""Конфигурация конструктора отчетов."""

    @abc.abstractproperty
    def async_task(self):
        u"""Асинхронная задача, в которой будет выполняться построение отчета.

        :rtype: :class:`celery.app.task.Task`
        """
    @abc.abstractproperty
    def current_user_func(self):
        u"""Функция, возвращающая текущего пользователя."""


# : Конфигурация конструктора отчетов.
# :
# : В проекте, который использует конструктор отчетов, в этой переменной должен
# : быть сохранен экземпляр потомка класса :class:`
#  ~constructor.config.ConstructorConfig`.
report_constructor_config = None
