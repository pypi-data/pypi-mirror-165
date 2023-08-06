# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [('report_constructor', '0004_reportfilter_fields'), ]

    operations = [
        migrations.AddField(
            model_name='reportcolumn',
            name='visible',
            field=models.BooleanField(
                default=True, verbose_name='Видимость колонки в отчете'), ),
    ]
