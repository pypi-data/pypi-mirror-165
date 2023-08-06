# coding: utf-8
from __future__ import absolute_import

from celery.result import states
import six


STATUS_PENDING = 1
STATUS_RECEIVED = 2
STATUS_STARTED = 3
STATUS_SUCCESS = 4
STATUS_REVOKED = 5
STATUS_FAILURE = 6
STATUS_RETRY = 7
STATUS_IGNORED = 8
STATUS_REJECTED = 9


# статусы в соответствии с состояниями задач celery
TASK_STATES = {
    STATUS_PENDING: states.PENDING,
    STATUS_RECEIVED: states.RECEIVED,
    STATUS_STARTED: states.STARTED,
    STATUS_SUCCESS: states.SUCCESS,
    STATUS_REVOKED: states.REVOKED,
    STATUS_FAILURE: states.FAILURE,
    STATUS_RETRY: states.RETRY,
    STATUS_IGNORED: states.IGNORED,
    STATUS_REJECTED: states.REJECTED,
}

# состояния задач celery по статусам
TASK_STATUSES = dict((v, k) for k, v in six.iteritems(TASK_STATES))


# отображение статусов
STATUS_CHOICES = (
    (STATUS_PENDING, u'Неизвестно'),
    (STATUS_RECEIVED, u'В очереди'),
    (STATUS_STARTED, u'Выполняется'),
    (STATUS_SUCCESS, u'Успешно выполнена'),
    (STATUS_REVOKED, u'Остановлена'),
    (STATUS_FAILURE, u'Ошибка'),
    (STATUS_RETRY, u'Перезапуск'),
    (STATUS_IGNORED, u'Игнорирована'),
    (STATUS_REJECTED, u'Отменена'),
)


def get_state_str(status_idx):
    return TASK_STATES[status_idx]


def get_status_idx(state_str):
    return TASK_STATUSES.get(state_str, STATUS_PENDING)
