# coding: utf-8
from __future__ import absolute_import

from datetime import datetime


def get_string_value(text):
    u"""Возвращает строковое значение."""
    text = text.replace(u'\n', u' ')
    while text.find(u'  ') != -1:
        text = text.replace(u'  ', u' ')
    return text


def get_int_value(text):
    u"""Возвращает числовое значение."""
    text = get_string_value(text)
    result = None
    if text:
        try:
            result = int(text)
        except ValueError:
            pass
    return result


def get_date_value(text, xml_format=False):
    u"""Возвращает значение даты.

    :param text basestring: Строковое значение поля.
    :param boolean xml_format: Флаг формата даты, принятой для типа данных
        date в XML Schema.
    """
    text = get_string_value(text)
    date_format = '%Y.%m.%d' if xml_format else '%d.%m.%Y'
    return datetime.strptime(text, date_format).date()


def get_bool_value(text):
    u"""Возвращает булевое значение."""
    text = get_string_value(text)
    return True if text.lower() == 'true' else False
