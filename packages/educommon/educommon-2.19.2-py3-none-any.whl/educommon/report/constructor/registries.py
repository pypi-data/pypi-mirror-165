# coding: utf-8
from __future__ import absolute_import

import six

from .base import ModelDataSourceParams


class DataSourceParamsRegistry(object):

    u"""Реестр параметров данных.

    При первом чтении из реестра отправляет сигнал ``init`` для добавления
    в реестр параметров для источников данных системы. Каждое django-приложение
    должно в обработчике этого сигнала зарегистрировать свои параметры
    источников данных.
    """

    def __init__(self):
        u"""Инициализация реестра.

        По завершении инициализации отправляет сигнал ``post_init``.
        """
        self._data_sources_params = {}

    def register(self, data_source_params):
        u"""Регистрация параметров источника данных."""
        assert isinstance(data_source_params, ModelDataSourceParams)
        assert data_source_params.name
        assert data_source_params.name not in self._data_sources_params

        self._data_sources_params[data_source_params.name] = data_source_params

    def get(self, data_source_name):
        u"""Возвращает параметры источника данных по имени.

        :param str data_source_name: Имя источника данных.
        """
        return self._data_sources_params[data_source_name]

    def __contains__(self, key):
        return key in self._data_sources_params

    def iterkeys(self):
        return six.iterkeys(self._data_sources_params)

    def itervalues(self):
        return six.itervalues(self._data_sources_params)

    def iteritems(self):
        return six.iteritems(self._data_sources_params)


registry = DataSourceParamsRegistry()
