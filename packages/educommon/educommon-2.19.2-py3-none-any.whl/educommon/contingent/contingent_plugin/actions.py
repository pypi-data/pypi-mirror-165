# coding: utf-8
from __future__ import absolute_import

from objectpack.actions import ObjectPack

from .models import ContingentModelChanged


class ContingentModelChangedPack(ObjectPack):

    title = u'Измененные объекты контингента'
    model = ContingentModelChanged

    columns = [
        {
            'data_index': 'content_type',
            'header': u'Тип'
        },
        {
            'data_index': 'content_object',
            'header': u'Объект'
        }
    ]

    def extend_menu(self, menu):
        return menu.SubMenu(
            u'Администрирование', menu.Item(
                self.title, self.list_window_action
            )
        )
