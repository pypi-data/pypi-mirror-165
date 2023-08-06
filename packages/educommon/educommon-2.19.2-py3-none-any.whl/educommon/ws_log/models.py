# coding: utf-8
u"""Модели приложения логирования СМЭВ."""
from __future__ import absolute_import

import datetime

from django.db import models
from django.db.models import Q
from django.db.models.expressions import Case
from django.db.models.expressions import Value
from django.db.models.expressions import When
from m3.db import BaseEnumerate
from m3.db import BaseObjectModel


class SmevSourceEnum(BaseEnumerate):
    u"""Источники взаимодействия."""

    EPGU = 0
    RPGU = 1
    INTER = 2
    BARS_OBR = 3
    CONCENTRATOR = 4
    MFC = 5

    SOURCE_TYPES = (
        (EPGU, u'ЕПГУ'),
        (RPGU, u'РПГУ'),
        (INTER, u'Межведомственное взаимодействие'),
        (BARS_OBR, u'Барс-Образование'),
        (CONCENTRATOR, u'Концентратор'),
        (MFC, u'МФЦ'),
    )

    values = dict(SOURCE_TYPES)


class ExtendedSmevLogManager(models.Manager):

    u"""Расширенный менеджер логов СМЭВ.

    Аннотирует дополнительные поля.
    """

    def get_queryset(self):
        query = super(ExtendedSmevLogManager, self).get_queryset()
        return query.annotate(
            # Пустые и null значения приведем к значению по умолчанию "Успешно"
            # для использования в фильтрации
            result_with_default=Case(
                When(
                    Q(result__isnull=True) | Q(result=''),
                    then=Value(SmevLog.RESULT_DEFAULT_VALUE)
                ),
                default='result'
            ),
        )


class SmevLog(BaseObjectModel):
    u"""Логи СМЭВ web-сервисов."""

    # Виды взаимодействия
    IS_SMEV = 0
    IS_NOT_SMEV = 1
    INTERACTION_TYPES = (
        (IS_SMEV, u'СМЭВ'),
        (IS_NOT_SMEV, u'Не СМЭВ'),
    )

    # Направление запроса
    INCOMING = 1
    OUTGOING = 0
    DIRECTION = (
        (INCOMING, u'Входящие запросы'),
        (OUTGOING, u'Исходящие запросы'),
    )

    # Потребители сервиса
    ENTITY = 0
    INDIVIDUAL = 1
    CONSUMER_TYPES = (
        (ENTITY, u'Юридическое лицо'),
        (INDIVIDUAL, u'Физическое лицо'),
    )

    # Источник взаимодействия
    EPGU = SmevSourceEnum.EPGU
    RPGU = SmevSourceEnum.RPGU
    INTER = SmevSourceEnum.INTER
    BARS_OBR = SmevSourceEnum.BARS_OBR
    SOURCE_TYPES = SmevSourceEnum.SOURCE_TYPES

    RESULT_DEFAULT_VALUE = u'Успешно'

    service_address = models.CharField(
        u'Адрес сервиса', max_length=250, null=True, blank=True)

    method_name = models.CharField(
        u'Код метода', max_length=250, null=True, blank=True, db_index=True)

    method_verbose_name = models.CharField(
        u'Наименование метода', max_length=250, null=True, blank=True)

    request = models.TextField(u'SOAP запрос', null=True, blank=True)
    response = models.TextField(u'SOAP ответ', null=True, blank=True)
    result = models.TextField(u'Результат', null=True, blank=True)

    time = models.DateTimeField(
        u'Время СМЭВ запроса', default=datetime.datetime.now, db_index=True)

    interaction_type = models.PositiveSmallIntegerField(
        u'Вид взаимодействия', choices=INTERACTION_TYPES, default=IS_SMEV)

    direction = models.SmallIntegerField(
        choices=DIRECTION,
        verbose_name=u'Направление запроса'
    )

    consumer_type = models.PositiveSmallIntegerField(
        u'Потребитель сервиса', choices=CONSUMER_TYPES, default=INDIVIDUAL,
        null=True, blank=True)

    consumer_name = models.CharField(
        u'Наименование потребителя', max_length=100, null=True, blank=True)

    source = models.PositiveSmallIntegerField(
        u'Источник взаимодействия', choices=SOURCE_TYPES,
        default=None, null=True, blank=True)

    target_name = models.CharField(
        u'Наименование электронного сервиса', max_length=100, null=True,
        blank=True)

    objects = models.Manager()
    extended_manager = ExtendedSmevLogManager()

    class Meta:
        verbose_name = u'Лог запросов СМЭВ'
        verbose_name_plural = u'Логи запросов СМЭВ'


class SmevProvider(BaseObjectModel):
    u"""Поставщики СМЭВ."""

    # Источник взаимодействия
    EPGU = SmevSourceEnum.EPGU
    RPGU = SmevSourceEnum.RPGU
    INTER = SmevSourceEnum.INTER
    CONCENTRATOR = SmevSourceEnum.CONCENTRATOR
    SOURCE_TYPES = SmevSourceEnum.SOURCE_TYPES

    mnemonics = models.CharField(u'Мнемоника', max_length=100)
    address = models.CharField(u'Адрес СМЭВ', max_length=100)
    source = models.PositiveSmallIntegerField(
        u'Источник взаимодействия', choices=SOURCE_TYPES)
    service_name = models.CharField(
        u'Наименование эл. сервиса', max_length=100)
    service_address_status_changes = models.CharField(
        u'Адрес сервиса изменения статуса', max_length=100,
        null=True, blank=True)
    entity = models.CharField(
        u'Наименование юр.лица', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = u'Поставщик СМЭВ'
        verbose_name_plural = u'Поставщики СМЭВ'
        unique_together = ('mnemonics', 'address')
