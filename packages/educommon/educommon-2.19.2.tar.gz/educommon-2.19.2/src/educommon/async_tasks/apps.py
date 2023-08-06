# coding: utf-8

from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):

    name = __package__
    label = 'async'
