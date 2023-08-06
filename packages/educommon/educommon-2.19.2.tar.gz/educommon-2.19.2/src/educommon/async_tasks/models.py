# coding: utf-8
u"""Модели для асинхронных задач Celery."""
from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.db import models
from m3.db import BaseObjectModel
from m3_django_compat.models import GenericForeignKey
from six import python_2_unicode_compatible

from educommon.django.db.mixins.validation import ModelValidationMixin

from . import statuses


@python_2_unicode_compatible
class AsyncTaskType(ModelValidationMixin, BaseObjectModel):

    u"""Модель типов асинхронных задач."""

    # предопределённые типы задач, хранятся в фикстурах
    TASK_UNKNOWN = 1
    TASK_SYSTEM = 2

    name = models.CharField(max_length=200, verbose_name=u'Тип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Тип асинхронных задач'
        verbose_name_plural = u'Типы асинхронных задач'


class AsyncTaskMeta(ModelValidationMixin, BaseObjectModel):

    u"""Модель данных асинхронных задач."""

    description = models.CharField(
        max_length=400,
        verbose_name=u'Описание задачи',
        null=True,
        blank=True
    )

    # путь класса от корня проекта, содержит имя модуля и название класса
    # пример для ЭДО: 'extedu.person.merge.tasks.MergeTask'
    location = models.CharField(
        max_length=400,
        verbose_name=u'Путь класса'
    )

    class Meta:
        verbose_name = u'Данные асинхронной задачи'
        verbose_name_plural = u'Данные асинхронных задач'


class RunningTask(ModelValidationMixin, BaseObjectModel):

    u"""Модель асинхронной задачи для отображения в соответствующем реестре."""

    # формат времени старта задачи
    STARTTIME_FORMAT = '%H:%M %d.m.%Y'
    # отображение пользователя, если пользователь не задан
    DEFAULT_USER = u'Система'

    MSG_TASK_NOT_FOUND = (
        u'Информации не найдено! Возможно задача была удалена!')

    content_type = models.ForeignKey(
        ContentType, null=True, blank=True, on_delete=models.SET_NULL
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    user = GenericForeignKey()
    task_id = models.CharField(
        max_length=36,
        verbose_name=u'ID задачи',
    )
    task_type = models.ForeignKey(
        AsyncTaskType,
        default=AsyncTaskType.TASK_UNKNOWN,
        verbose_name=u'Тип задачи',
        on_delete=models.CASCADE
    )
    task_meta = models.ForeignKey(
        AsyncTaskMeta,
        verbose_name=u'Данные задачи',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    status = models.SmallIntegerField(
        choices=statuses.STATUS_CHOICES,
        default=statuses.STATUS_PENDING,
        verbose_name=u'Состояние задачи',
        db_index=True
    )
    queued_on = models.DateTimeField(
        verbose_name=u'Старт задачи',
        db_index=True,
        null=True  # null - если задача ещё не в работе
    )

    class Meta:
        verbose_name = u'Асинхронная задача'
        verbose_name_plural = u'Асинхронные задачи'
