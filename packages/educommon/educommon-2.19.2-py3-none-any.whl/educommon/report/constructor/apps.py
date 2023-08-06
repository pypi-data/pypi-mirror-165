# coding: utf-8
from __future__ import absolute_import

from django.apps import config
from django.db.models import CharField
from django.db.models import TextField
from django.db.models.functions import Lower


class AppConfig(config.AppConfig):

    name = __name__.rpartition('.')[0]
    label = 'report_constructor'

    def ready(self):
        CharField.register_lookup(Lower)
        TextField.register_lookup(Lower)
