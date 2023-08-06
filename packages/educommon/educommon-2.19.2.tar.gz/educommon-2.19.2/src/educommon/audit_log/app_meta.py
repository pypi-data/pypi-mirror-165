# coding: utf-8
from __future__ import absolute_import

from educommon import ioc

from .actions import AuditLogPack
from .error_log.actions import PostgreSQLErrorPack


def register_actions():
    ioc.get('main_controller').packs.extend((
        AuditLogPack(),
        PostgreSQLErrorPack(),
    ))
