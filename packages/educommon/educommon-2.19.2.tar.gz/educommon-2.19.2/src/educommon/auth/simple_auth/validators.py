# coding: utf-8
from __future__ import absolute_import


class DefaultPasswordValidator(object):

    u"""Валидация пароля."""

    _validators = []

    def validate(self, password):
        return [validator(password) for validator in self._validators]
