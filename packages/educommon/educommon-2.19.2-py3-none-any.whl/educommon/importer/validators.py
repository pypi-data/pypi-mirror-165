# coding: utf-8
"""
Базовые валидаторы для импортируемых данных.

Использовать только для расширения/исправления логики, реализованной с помощью
`educommon.importer`. При написании новых классов для импорта/экспорта данных
рекомендуется использовать пакет `data-transfer`.
"""
from __future__ import absolute_import

from abc import ABCMeta
from abc import abstractmethod

from six import with_metaclass


class IImportDataValidator(with_metaclass(ABCMeta, object)):
    """
    Базовый класс валидатора импортируемых данных.
    """

    def __call__(self, data_row, errors, warnings):
        """
        Валидирует строку входных данных.

        :param data_row: словарь, представляющий одну строку импортируемых
        данных
        :param errors: Список ошибок, возникших в ходе валидации.
        :param warnings: Список предупреждений, возникших в ходе валидации.
        """
        raise NotImplementedError()
