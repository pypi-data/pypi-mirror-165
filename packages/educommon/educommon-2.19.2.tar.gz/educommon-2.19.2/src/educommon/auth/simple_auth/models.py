# coding: utf-8
from __future__ import absolute_import

from django.db import models
from m3_django_compat import AUTH_USER_MODEL


class ResetPasswords(models.Model):

    u"""Сброшенные пароли."""

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name=u'Пользователь',
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        u'Код восстановления',
        max_length=32,
        unique=True,
    )
    date = models.DateTimeField(
        u'Дата сброса пароля',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = u'Сброшенный пароль'
        verbose_name_plural = u'Сброшенные пароли'
