# coding: utf-8
from __future__ import absolute_import

from educommon import ioc

from .editor.actions import Pack


def register_actions():
    ioc.get('main_controller').packs.extend((
        Pack(),
    ))
