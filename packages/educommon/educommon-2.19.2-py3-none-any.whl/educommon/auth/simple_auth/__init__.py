# coding: utf-8
from __future__ import absolute_import

from . import const


# Например, settings.LOGIN_URL = simple_auth.get_login_url()
def get_login_url():
    return ''.join((
        const.AUTH_CONTROLLER_URL,
        const.AUTH_PACK_URL,
        const.LOGIN_PAGE_URL
    ))
