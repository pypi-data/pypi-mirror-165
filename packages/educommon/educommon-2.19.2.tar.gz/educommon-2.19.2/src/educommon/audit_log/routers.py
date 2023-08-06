# coding: utf-8
from __future__ import absolute_import

from educommon.django.db.routers import ServiceDbRouterBase


class AuditLogRouter(ServiceDbRouterBase):
    app_name = 'audit_log'
    service_db_model_names = {'AuditLog', 'LogProxy', 'Table'}
