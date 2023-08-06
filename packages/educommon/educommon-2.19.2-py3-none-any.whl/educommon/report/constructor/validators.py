# coding: utf-8
from __future__ import absolute_import

from django.core.exceptions import ValidationError

from .registries import registry


def validate_data_source_name(value):
    u"""Валидатор для имен источников данных.

    Источник данных должен быть зарегистрирован в реестре.
    """
    if value not in registry:
        raise ValidationError(
            u'Источник данных "{}" не существует.'.format(value)
        )
