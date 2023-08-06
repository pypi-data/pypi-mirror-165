# coding: utf-8
from __future__ import absolute_import


class ReportConstructorException(Exception):

    u"""Базовый класс для исключений конструктора отчетов."""


class DataSourceParamsNotFound(ReportConstructorException):
    u"""Исключение при отсутствии в реестре параметров источника данных."""

    def __init__(self, data_source_name):
        self.data_source_name = data_source_name

        super(DataSourceParamsNotFound, self).__init__(
            u'"Параметры для источника данных с именем "{}" не '
            u'зарегистрированы в системе.'.format(self.data_source_name.name)
        )


class FilterError(ReportConstructorException):

    u"""Ошибка в фильтре."""

    def __init__(self, report_filter, message):
        self.report_filter = report_filter

        if not message:
            message = (
                u'Ошибка в фильтре для столбца {}'
                .format(self.report_filter.column.title)
            )

        super(FilterError, self).__init__(
            u'Ошибка в фильтре для столбца {}: {}'.format(
                self.report_filter.column.title, message
            )
        )
