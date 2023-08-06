# coding: utf-8
from __future__ import absolute_import


# -----------------------------------------------------------------------------
# Источники разрешений

PERM_SOURCE__ROLE = 1
PERM_SOURCE__NESTED_ROLE = 2
PERM_SOURCE__DEPENDENCIES = 3


PERM_SOURCES = {
    PERM_SOURCE__ROLE: u'Редактируемая роль',
    PERM_SOURCE__NESTED_ROLE: u'Вложенные роли',
    PERM_SOURCE__DEPENDENCIES: u'Зависимые разрешения',
}
# -----------------------------------------------------------------------------
