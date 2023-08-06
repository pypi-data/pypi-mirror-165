# coding: utf-8
from __future__ import absolute_import

from educommon import ioc

from .actions import OkoguPack
from .actions import OKSMPack


def register_actions():
    u"""Регистрация паков."""
    ioc.get('main_controller').extend_packs((
        OkoguPack(),
        OKSMPack()
    ))
