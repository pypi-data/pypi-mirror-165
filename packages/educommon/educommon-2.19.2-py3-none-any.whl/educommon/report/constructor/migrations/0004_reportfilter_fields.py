# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations
from django.db import models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [('report_constructor', '0003_reportfilter_exclude'), ]

    operations = [
        migrations.AlterField(
            model_name='reportfilter',
            name='operator',
            field=models.PositiveSmallIntegerField(
                choices=[(1, 'Меньше или равно'),
                         (2, 'Меньше'),
                         (3, 'Равно'),
                         (4, 'Больше'),
                         (5, 'Больше или равно'),
                         (6, 'Пусто'),
                         (7, 'Содержит'),
                         (8, 'Начинается с'),
                         (9, 'Заканчивается на'),
                         (10, 'Между'),
                         (11, 'Равно одному из')],
                verbose_name='Оператор сравнения'), ),
        migrations.AlterField(
            model_name='reportfilter',
            name='values',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.TextField(verbose_name='Значение'),
                blank=True,
                null=True,
                size=None), ),
    ]
