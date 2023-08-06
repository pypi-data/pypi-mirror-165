# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import codecs
import os.path

from django.conf import settings
from django.db import connections
from django.db import migrations
from django.db.migrations.operations.base import Operation

from ..constants import EXCLUDED_TABLES
from ..constants import PG_LOCK_ID
from ..constants import SQL_FILES_DIR
from ..utils import get_db_connection_params


class InitDefaultDatabase(Operation):

    u"""Настраивает основную БД."""

    reversible = True

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state,
                          to_state):
        if schema_editor.connection.alias != settings.DEFAULT_DB_ALIAS:
            return

        params = get_db_connection_params()
        params['lock_id'] = PG_LOCK_ID

        sql_file_path = os.path.join(SQL_FILES_DIR, 'install_audit_log.sql')
        with codecs.open(sql_file_path, 'r', 'utf-8') as sql_file:
            sql = sql_file.read().replace('%', '%%').format(**params)

        schema_editor.execute(sql)

    def database_backwards(self, app_label, schema_editor, from_state,
                           to_state):
        if schema_editor.connection.alias != settings.DEFAULT_DB_ALIAS:
            return

        sql_file_path = os.path.join(SQL_FILES_DIR, 'uninstall_audit_log.sql')
        with codecs.open(sql_file_path, 'r', 'utf-8') as sql_file:
            sql = sql_file.read().replace('%', '%%')

        schema_editor.execute(sql)


class LoadTableData(Operation):

    u"""Заполняет данными модель Table."""

    reversible = True

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state,
                          to_state):
        Table = to_state.apps.get_model('audit_log', 'Table')

        if self.allow_migrate_model(schema_editor.connection.alias, Table):
            cursor = connections[settings.DEFAULT_DB_ALIAS].cursor()
            cursor.execute('\n'.join((
                "SELECT table_name, table_schema",
                "FROM information_schema.tables",
                "WHERE table_schema = 'public'",
            )))

            for name, schema in cursor:
                if (schema, name) not in EXCLUDED_TABLES:
                    Table.objects.get_or_create(name=name, schema=schema)

    def database_backwards(self, app_label, schema_editor, from_state,
                           to_state):
        pass


class Migration(migrations.Migration):

    u"""Инициализация подсистемы журналирования изменений в БД."""

    dependencies = [
        ('audit_log', '0001_initial'),
    ]

    operations = [
        InitDefaultDatabase(),
        LoadTableData(),
    ]
