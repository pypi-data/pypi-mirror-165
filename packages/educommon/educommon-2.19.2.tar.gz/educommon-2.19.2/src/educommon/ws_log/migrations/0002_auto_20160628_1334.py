# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('ws_log', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='smevprovider',
            name='service_address_status_changes',
            field=models.CharField(default='', max_length=100, verbose_name='Адрес сервиса изменения статуса'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='smevprovider',
            name='service_name',
            field=models.CharField(default='', max_length=100, verbose_name='Наименование эл. сервиса'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='smevprovider',
            unique_together=set([('mnemonics', 'address')]),
        ),
    ]
