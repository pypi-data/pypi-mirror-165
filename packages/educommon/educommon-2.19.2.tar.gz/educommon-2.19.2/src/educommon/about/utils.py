# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from os.path import normcase
from os.path import realpath
import sys

from pkg_resources import working_set


def get_installed_distributions():
    """Возвращает информацию об установленных в окружении пакетах.

    :rtype: list of :class:`~pkg_resources.Distribution`.
    """
    stdlib_pkgs = ('python', 'wsgiref', 'argparse',)

    # pylint: disable=not-an-iterable
    for dist in working_set:
        if (
            dist.key not in stdlib_pkgs and
            normcase(realpath(dist.location)).startswith(realpath(sys.prefix))
        ):
            yield dist
