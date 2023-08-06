# coding: utf-8
from __future__ import absolute_import

from datetime import datetime

from celery.signals import before_task_publish
from celery.signals import task_postrun
from celery.signals import task_prerun
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import HStoreField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.backends.signals import connection_created
from django.dispatch.dispatcher import receiver
import six

from educommon.django.db.models import BaseModel
from educommon.django.db.models import ReadOnlyMixin
from educommon.thread_data import thread_data

from .utils import get_audit_log_context
from .utils import get_model_by_table
from .utils import set_db_param


class Table(ReadOnlyMixin, BaseModel):

    name = models.CharField(
        max_length=250,
        verbose_name=u'Имя таблицы'
    )
    schema = models.CharField(
        max_length=250,
        verbose_name=u'Схема таблицы'
    )

    class Meta:
        unique_together = ('name', 'schema')
        verbose_name = u'Логируемая таблица'
        verbose_name_plural = u'Логируемые таблицы'


class AuditLog(ReadOnlyMixin, BaseModel):

    OPERATION_CREATE = 1
    OPERATION_UPDATE = 2
    OPERATION_DELETE = 3
    OPERATION_CHOICES = (
        (OPERATION_CREATE, u'Создание'),
        (OPERATION_UPDATE, u'Изменение'),
        (OPERATION_DELETE, u'Удаление')
    )

    user_id = models.IntegerField(
        null=True,
        db_index=True,
        verbose_name=u'Пользователь',
    )
    user_type_id = models.IntegerField(
        null=True,
        db_index=True,
        verbose_name=u'Тип пользователя',
    )
    ip = models.GenericIPAddressField(
        null=True,
        verbose_name=u'IP адрес'
    )
    time = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=u'Дата, время'
    )
    table = models.ForeignKey(
        Table,
        verbose_name=u'Таблица',
        on_delete=models.CASCADE,
    )
    object_id = models.IntegerField(
        db_index=True,
        verbose_name=u'Объект модели'
    )
    data = HStoreField(
        null=True,
        verbose_name=u'Объект'
    )
    changes = HStoreField(
        null=True,
        verbose_name=u'Изменения'
    )
    operation = models.SmallIntegerField(
        choices=OPERATION_CHOICES,
        verbose_name=u'Действие'
    )

    def is_read_only(self):
        u"""Запрещает запись в лог приложению."""
        return True

    def get_read_only_error_message(self, delete):
        action_text = u'удалить' if delete else u'изменить'
        result = u'Нельзя {} запись лога.'.format(action_text)
        return result

    @property
    def model(self):
        u"""Класс измененной модели."""
        return get_model_by_table(self.table)

    @property
    def fields(self):
        u"""Все поля измененной модели.

        :returns dict: {имя колонки в БД: поле, ...}
        """
        model = self.model
        if model:
            result = {
                field.get_attname_column()[1]: field
                for field in model._meta.fields
            }
            return result

    @property
    def user(self):
        u"""Пользователь, внесший изменения."""
        result = None
        try:
            content_type = ContentType.objects.get(id=self.user_type_id)
        except ContentType.DoesNotExist:
            pass
        else:
            model_class = content_type.model_class()
            if model_class:
                try:
                    return model_class.objects.get(pk=self.user_id)
                except model_class.DoesNotExist:
                    pass

        return result

    class Meta:
        verbose_name = u'Запись журнала изменений'
        verbose_name_plural = u'Записи журнала изменений'


class PostgreSQLError(BaseModel):

    u"""Журнал ошибок, возникающих при работе триггеров журнала изменений."""

    user_id = models.IntegerField(
        u'Пользователь',
        null=True,
    )
    ip = models.GenericIPAddressField(
        u'IP адрес',
        null=True,
    )
    time = models.DateTimeField(
        u'Дата, время',
        auto_now_add=True,
        validators=[MinValueValidator(datetime(1900, 1, 1))],
    )
    level = models.CharField(
        u'Уровень ошибки',
        max_length=50,
    )
    text = models.TextField(
        u'Текст ошибки',
    )

    class Meta:
        verbose_name = u'Ошибка PostgreSQL'
        verbose_name_plural = u'Ошибки PostgreSQL'
        db_table = 'audit"."postgresql_errors'


class LoggableModelMixin(models.Model):
    """Делает модель логируемой."""
    need_to_log = True

    class Meta:
        abstract = True
# -----------------------------------------------------------------------------
# Передача параметров контекста журналирования изменений в задания Celery.

# Именно такой способ передачи параметров контекста журналирования изменений
# выбран в связи с особенностями Celery, которые заключаются в том, что
# обработчики сигналов task_prerun, task_postrun и само задание выполняются в
# отдельных подключениях к БД, соответственно из обработчиков этих сигналов
# установить параметры нет возможности.


_package_name = __name__.rpartition('.')[0]


@before_task_publish.connect(dispatch_uid=_package_name + 'save')
def _save_audit_log_context_for_task(body, **_):
    u"""Дополняет параметры задания данными для журнала изменений.

    В словарь ``kwargs``, передаваемый в метод ``apply_async`` задания,
    добавляет параметр ``audit_log_params``, содержащий результат вызова
    функции :func:`~extedu.audit_log.utils.get_audit_log_context`.

    Работает только если запуск задания осуществляется в рамках обработки
    HTTP-запроса, т.е. если в :obj:`extedu.thread_data.http_request` сохранен
    HTTP-запрос.
    """
    if not hasattr(thread_data, 'http_request'):
        return

    body['kwargs'] = body.get('kwargs', {})
    request = thread_data.http_request
    body['kwargs']['audit_log_params'] = get_audit_log_context(request)


@task_prerun.connect(dispatch_uid=_package_name + 'set')
def _set_audit_log_context_for_task(kwargs, **_):
    u"""До выполнения задания сохраняет параметры контекста журнала изменений.

    Сохраненные в :obj:`extedu.thread_data.audit_log_params` параметры
    будут переданы в БД при подключении (см.
    ``_send_audit_log_context_to_db``).
    """
    if 'audit_log_params' in kwargs:
        thread_data.audit_log_params = kwargs['audit_log_params']


@task_postrun.connect(dispatch_uid=_package_name + 'unset')
def _unset_audit_log_context_for_task(task, kwargs, **_):
    if hasattr(thread_data, 'audit_log_params'):
        del thread_data.audit_log_params


@receiver(connection_created, dispatch_uid=_package_name + 'send')
def _send_audit_log_context_to_db(**kwargs):
    if hasattr(thread_data, 'audit_log_params'):
        for name, value in six.iteritems(thread_data.audit_log_params):
            set_db_param('audit_log.' + name, value)
# -----------------------------------------------------------------------------
