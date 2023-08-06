# coding: utf-8
from __future__ import absolute_import


PERM_GROUP__ROLE = 'role'

PERM__ROLE__VIEW = PERM_ROLE_VIEW = PERM_GROUP__ROLE + '/view'
PERM__ROLE__EDIT = PERM_ROLE_EDIT = PERM_GROUP__ROLE + '/edit'
# -----------------------------------------------------------------------------


permissions = (
    (PERM__ROLE__VIEW,
     u'Просмотр ролей',
     u'Разрешает просмотр имеющихся в системе ролей.'),
    (PERM__ROLE__EDIT,
     u'Редактирование ролей',
     u'Разрешает создавать/изменять/удалять роли и назначать ролям '
     u'разрешения.'),
)
# -----------------------------------------------------------------------------

dependencies = {
    PERM__ROLE__EDIT: {
        PERM__ROLE__VIEW,
    },
}
# -----------------------------------------------------------------------------
