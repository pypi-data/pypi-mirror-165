# coding: utf-8
from __future__ import absolute_import

from spyne.error import Fault
import six


class SpyneException(Fault):
    u"""Переопределенный Exception базового exception`а spyne.

    По спецификации спайна faultcode
    It's a dot-delimited string whose first fragment is
            either 'Client' or 'Server'.
    """
    def __init__(self, code=0, message=''):
        if isinstance(code, six.string_types):
            Fault.__init__(self, faultstring=code)
        else:
            Fault.__init__(self,
                           faultcode='Server;%d' % code,
                           faultstring=message)
