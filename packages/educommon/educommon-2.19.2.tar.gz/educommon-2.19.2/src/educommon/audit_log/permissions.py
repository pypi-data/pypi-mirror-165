# coding: utf-8
from __future__ import absolute_import


PERM_GROUP__AUDIT_LOG = 'audit_log'
PERM_GROUP__AUDIT_LOG_ERRORS = 'audit_log_errors'


PERM__AUDIT_LOG__VIEW = PERM_GROUP__AUDIT_LOG + '/view'
PERM__AUDIT_LOG__ERRORS__VIEW = PERM_GROUP__AUDIT_LOG_ERRORS + '/view'
PERM__AUDIT_LOG__ERRORS__DELETE = PERM_GROUP__AUDIT_LOG_ERRORS + '/delete'


permissions = (
    (PERM__AUDIT_LOG__VIEW,
     u'Просмотр',
     u'Разрешает просмотр журнала изменений.'),
    (PERM__AUDIT_LOG__ERRORS__VIEW,
     u'Просмотр журнала ошибок PostgreSQL',
     u'Разрешает просмотр журнала ошибок PostgreSQL.'),
    (PERM__AUDIT_LOG__ERRORS__DELETE,
     u'Удаление записей журнала ошибок PostgreSQL',
     u'Разрешает удаление записей из журнала ошибок PostgreSQL.'),
)


dependencies = {
    PERM__AUDIT_LOG__ERRORS__DELETE: {
        PERM__AUDIT_LOG__ERRORS__VIEW,
    },
}


groups = {
    PERM_GROUP__AUDIT_LOG: u'Журнал изменений',
    PERM_GROUP__AUDIT_LOG_ERRORS: u'Журнал изменений',
}


partitions = {
    u'Администрирование': (
        PERM_GROUP__AUDIT_LOG,
        PERM_GROUP__AUDIT_LOG_ERRORS,
    ),
}
