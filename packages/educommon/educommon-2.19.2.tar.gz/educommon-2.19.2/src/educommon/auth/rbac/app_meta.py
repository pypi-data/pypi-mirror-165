# coding: utf-8
u"""Инициализация приложения в M3."""
from __future__ import absolute_import

from educommon import ioc

from . import actions


def register_actions():
    u"""Регистрация паков приложения в контроллере."""
    ioc.get('auth_controller').extend_packs((
        actions.Pack(),
        actions.PartitionsPack(),
        actions.PermissionsPack(),
        actions.ResultPermissionsPack(),
    ))
