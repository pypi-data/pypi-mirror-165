# coding: utf-8
from __future__ import unicode_literals

from educommon.django.db.model_view import AttrValue
from educommon.django.db.model_view import HtmlTableView
from educommon.django.db.model_view import Text


related_model_views = (
    HtmlTableView(
        model='contingent_plugin.ContingentModelChanged',
        description=Text('Измененная модель'),
        columns=(
            dict(
                header=Text('Идентификатор объекта'),
                data=AttrValue('object_id')
            ),
        )
    ),
    HtmlTableView(
        model='contingent_plugin.ContingentModelDeleted',
        description=Text('Удаленная модель'),
        columns=(
            dict(
                header=Text('Идентификатор объекта'),
                data=AttrValue('object_id')
            ),
        )
    ),
)
