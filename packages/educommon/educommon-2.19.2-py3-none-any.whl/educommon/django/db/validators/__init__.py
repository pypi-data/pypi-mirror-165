# coding: utf-8
u"""Валидаторы для полей моделей Django.

Документация: http://djbook.ru/rel1.4/ref/validators.html
"""
from __future__ import absolute_import

from abc import ABCMeta
from abc import abstractmethod

from django.core.exceptions import ValidationError
from six import with_metaclass


def validate_value(value, validator):
    u"""Выполняет проверку значения value с помощью валидатора validator.

    Удобно использовать при проверке валидаторами значений вне модели,
    например так:

        from functools import partial
        is_snils_valid = partial(validate_value, validator=snils_validator)
        if is_snils_valid('064-949-063 00'):
            print 'Ok'

    :param value: Проверяемое значение.
    :param validator: Валидатор для моделей Django, callable-объект,
        принимающий один аргумент (проверяемое значение) и генерирующий
        исключение django.core.exceptions.ValidationError в случае, если
        указанное значение не прошло проверку.

    :return: Если проверка пройдена, возвращает True, иначе False.
    :rtype: bool
    """
    try:
        validator(value)
    except ValidationError:
        return False
    else:
        return True


class IModelValidator(with_metaclass(ABCMeta, object)):
    u"""Базовый класс валидатора модели."""

    @abstractmethod
    def clean(self, instance, errors):
        u"""Валидирует объект.

        :param instance: экземпляр проверяемой модели.
        :type instance: django.db.models.base.Model

        :param errors: ошибки, выявленные в ходе проверки.
        :type errors: collections.OrderedDict
        """
        raise NotImplementedError()
