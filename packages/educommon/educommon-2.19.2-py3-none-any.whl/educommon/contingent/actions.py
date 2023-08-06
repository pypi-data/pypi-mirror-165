# coding: utf-8
u"""Паки справочников контингента."""
from __future__ import absolute_import

from django.db.models import Q
from objectpack.actions import ObjectPack

from .catalogs import OkoguVirtualModel
from .catalogs import OksmVirtialModel


class OkoguPack(ObjectPack):
    u"""Пак, предоставляющий средства для просмотра справочника ОКОГУ."""

    title = u'ОКОГУ'

    model = OkoguVirtualModel

    columns = [
        dict(
            data_index='id',
            header=u'Код',
            width=1,
            searchable=True,
        ),
        dict(
            data_index='full_name',
            header=u'Полное наименование',
            width=3,
            searchable=True,
        ),
        dict(
            data_index='short_name',
            header=u'Сокращенное наименование',
            width=2,
            searchable=True,
        ),
    ]
    list_sort_order = ('id',)
    column_name_on_select = 'full_name'

    def configure_grid(self, grid):
        u"""Конфигурирование грида.

        Добавляется css класс для переноса строк в ячейках грида
        """
        super(OkoguPack, self).configure_grid(grid)

        grid.cls = 'word-wrap-grid'  # перенос строк в ячейках грида


class OKSMPack(ObjectPack):
    u"""Справочник ОКСМ."""

    title = u'Справочник ОКСМ'
    model = OksmVirtialModel
    read_only = True
    list_sort_order = ['shortname']
    column_name_on_select = 'shortname'

    columns = [
        {
            'data_index': 'shortname',
            'header': u'Краткое наименование страны',
            'sortable': True,
            'searchable': True,
            'width': 2
        },
        {
            'data_index': 'code',
            'header': u'Код',
            'sortable': True,
            'searchable': True,
            'width': 1
        },
        {
            'data_index': 'full_name',
            'header': u'Полное наименование',
            'sortable': True,
            'searchable': True,
            'width': 3
        }
    ]

    def get_rows_query(self, request, context):
        u"""
        Метод выполняет фильтрацию QuerySet.

        Исключается отображение РФ.
        """
        records = super(OKSMPack, self).get_rows_query(request, context)

        return records.exclude(code=OksmVirtialModel.rf_code)

    def apply_search(self, query, request, context):
        u"""Поиск по краткому наименованию или коду."""
        query = super(
            OKSMPack, self).apply_search(query, request, context)

        if hasattr(context, 'filter'):
            query = query.filter(Q(shortname__icontains=context.filter) |
                                 Q(code=context.filter))
        return query
