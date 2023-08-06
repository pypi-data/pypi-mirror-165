# coding: utf-8
from __future__ import absolute_import

from django.conf.urls import url
from m3.actions import ControllerCache
from m3_ext.ui.app_ui import GENERIC_USER
from m3_ext.ui.app_ui import DesktopLoader
from m3_ext.ui.app_ui import DesktopShortcut
from objectpack.desktop import uificate_the_controller

from educommon import ioc

from .actions import AuthPack


auth_controller = ioc.get('auth_controller')


def register_actions():
    auth_controller.extend_packs((
        AuthPack(),
    ))


def register_desktop_menu():
    u"""Добавляет в меню Пуск пункт "Выход"."""
    auth_pack = ControllerCache.find_pack(AuthPack)
    DesktopLoader.add(
        GENERIC_USER,
        DesktopLoader.TOOLBOX,
        DesktopShortcut(
            pack=auth_pack.logout_confirm_action,
            name=u'Выход',
            index=256,
            icon='logout'
        )
    )

    uificate_the_controller(auth_controller)


def register_urlpatterns():
    u"""Регистрация URL контроллера."""
    return [
        url(*auth_controller.urlpattern),
    ]
