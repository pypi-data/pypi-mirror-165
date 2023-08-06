# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [('report_constructor', '0005_reportcolumn_visible'), ]

    operations = [
        migrations.CreateModel(
            name='ReportSorting',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('direction', models.PositiveSmallIntegerField(
                    choices=[(1, 'По возрастанию'), (2, 'По убыванию')],
                    verbose_name='Направление сортировки')),
                ('index', models.PositiveSmallIntegerField(
                    verbose_name='Порядковый номер')),
                ('column', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='report_constructor.ReportColumn',
                    verbose_name='Колонка')),
            ],
            options={
                'verbose_name': 'Сортировка',
                'verbose_name_plural': 'Сортировка',
            }, ),
    ]
