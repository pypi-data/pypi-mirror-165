# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audit_log', '0002_install_audit_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('audit_log.auditlog',),
        ),
    ]
