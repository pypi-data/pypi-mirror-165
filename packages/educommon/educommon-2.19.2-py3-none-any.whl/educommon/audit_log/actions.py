# coding: utf-8
from __future__ import absolute_import

from datetime import date
from datetime import timedelta
from functools import partial

from django.contrib.postgres.fields.hstore import HStoreField
from django.db.models import GenericIPAddressField
from m3.actions.results import PreJsonResult
from m3_ext.ui.all_components import ExtStringField
from objectpack.actions import BaseAction
from objectpack.actions import ObjectPack
from objectpack.filters import ColumnFilterEngine
from objectpack.ui import make_combo_box

from educommon import ioc
from educommon.m3 import PackValidationMixin
from educommon.objectpack.actions import ViewWindowPackMixin
from educommon.utils.ui import DatetimeFilterCreator
from educommon.utils.ui import FilterByField

from .permissions import PERM_GROUP__AUDIT_LOG
from .proxies import LogProxy
from .ui import ViewChangeWindow
from .utils import get_model_choices
from .utils import make_hstore_filter
from .utils import make_name_filter


class AuditLogPack(ViewWindowPackMixin, PackValidationMixin, ObjectPack):

    u"""Журнал изменений."""

    title = u'Журнал изменений'
    model = LogProxy
    width = 1000
    height = 600
    allow_paging = True

    list_sort_order = ('-time',)

    filter_engine_clz = ColumnFilterEngine
    ff = partial(FilterByField, model, model_register=ioc.get('observer'))

    edit_window = ViewChangeWindow

    can_delete = False

    # Фильтр интервала дат
    date_filter = DatetimeFilterCreator(
        model, 'time',
        get_from=lambda: date.today() - timedelta(days=2),
        get_to=date.today
    )

    columns = [
        {
            'data_index': 'time',
            'width': 140,
            'header': u'Дата и время',
            'sortable': True,
            'filter': date_filter.filter
        },
        {
            'data_index': 'user_name',
            'width': 130,
            'header': u'Пользователь',
            'filter': ff(
                'table__name',
                lookup=lambda x: make_name_filter('surname', x)
            ) & ff(
                'table__name',
                lookup=lambda x: make_name_filter('firstname', x)
            ) & ff(
                'table__name',
                lookup=lambda x: make_name_filter('patronymic', x)
            )
        },
        {
            'data_index': 'operation',
            'width': 60,
            'header': u'Операция',
            'filter': ff(
                'operation',
                ask_before_deleting=False
            ),
        },
        {
            'data_index': 'model_name',
            'width': 220,
            'header': u'Модель объекта',
            'filter': ff(
                'table',
                control_creator=lambda: make_combo_box(
                    data=get_model_choices(),
                    ask_before_deleting=False,
                ),
            ),
        },
        {
            'data_index': 'object_id',
            'width': 50,
            'header': u'Код объекта',
            'filter': ff('object_id'),
        },
        {
            'data_index': 'ip',
            'width': 60,
            'header': u'IP',
            'filter': ff(
                'ip',
                parser_map=(GenericIPAddressField, 'unicode', '%s__contains'),
                control_creator=ExtStringField,
            ),
        },
        {
            'data_index': 'object_string',
            'width': 180,
            'header': u'Объект',
            'filter': ff(
                'data',
                parser_map=(HStoreField, 'unicode', '%s__values__icontains'),
                lookup=lambda x: make_hstore_filter('data', x),
                control_creator=ExtStringField,
            ),
        },
    ]

    def __init__(self):
        super(AuditLogPack, self).__init__()
        self.view_changes_action = ViewChangeAction()
        self.actions.append(self.view_changes_action)

        self.need_check_permission = True
        self.perm_code = PERM_GROUP__AUDIT_LOG

        for action in self.actions:
            action.perm_code = 'view'

    def configure_grid(self, grid):
        u"""Настройка грида.

        Устанавливает интервал дат фильтрации по умолчанию
        в параметрах запроса.
        """
        super(AuditLogPack, self).configure_grid(grid)
        grid.store.base_params = self.date_filter.base_params

    def get_edit_window_params(self, params, request, context):
        params = super(AuditLogPack, self).get_edit_window_params(
            params, request, context
        )
        params['grid_action'] = self.view_changes_action
        return params

    def get_list_window_params(self, params, request, context):
        params = super(AuditLogPack, self).get_list_window_params(
            params, request, context
        )
        params['maximized'] = True
        return params

    def get_rows_query(self, request, context):
        return super(AuditLogPack, self).get_rows_query(
            request, context
        ).prefetch_related('table')

    def extend_menu(self, menu):
        return menu.administry(
            menu.Item(self.title, self.list_window_action),
        )


class ViewChangeAction(BaseAction):

    u"""Action для просмотра изменений."""

    def context_declaration(self):
        result = super(ViewChangeAction, self).context_declaration()
        result[self.parent.id_param_name] = dict(type='int')
        return result

    def run(self, request, context):
        object_id = getattr(context, self.parent.id_param_name)
        if object_id:
            rows = LogProxy.objects.get(id=object_id).diff
        else:
            rows = []
        return PreJsonResult({'rows': rows, 'total': len(rows)})
