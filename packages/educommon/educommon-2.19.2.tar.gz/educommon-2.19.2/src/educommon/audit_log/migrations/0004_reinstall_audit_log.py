# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations

from ..utils.operations import ReinstallAuditLog


class Migration(migrations.Migration):

    dependencies = [
        ('audit_log', '0003_logproxy'),
    ]

    operations = [
        ReinstallAuditLog()
    ]
