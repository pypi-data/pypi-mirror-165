# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function

from importlib import import_module
from optparse import make_option
import inspect
import os

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.db import connection
from django.db.models.base import ModelBase
from django.db.models.fields.files import FileDescriptor
from m3_django_compat import commit_unless_managed
from six.moves import zip
import six

from educommon.django.storages.atcfs.api import AtcfsApi


def dictfetchall(cursor):
    """
    Вспомогательная функция.
    cursor.fetchall возвращает данные в виде списка списков:
    (('43', 'text 1'), ('44', 'text 2'), ('45', 'text 3'))
    Эта функция преобразует в вид:
    [{'id': '43', 'field': 'text 1'}, ('id': '44', 'field': 'text 2'), ...]
    :param cursor: куросор на выполненный запрос к БД
    :return: список словарей
    """
    desc = cursor.description
    columns = [col[0] for col in desc]
    return [dict(list(zip(columns, row))) for row in cursor.fetchall()]


class Command(NoArgsCommand):
    """
    Команда обходит все зарегистрированные модели,
    в которых есть поля FileField.
    Если для поля установлен AtcfsStorage, или он установлен глобально,
    то файл переносится на сервер ATCFS.
    """

    option_list = NoArgsCommand.option_list + (
        make_option(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help=u'Удалять файлы вместо перемещения.'
        ),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.api = AtcfsApi()

    def _get_fields(self, model):
        """
        Выбираем в модели все переменные, являющиеся FileField-полями.
        :param model: класс модели
        :return: список названий полей FileField
        """
        fields = []
        for nam, mem in six.iteritems(model.__dict__):
            if callable(mem):
                continue
            if nam.startswith('_'):
                continue
            if isinstance(mem, FileDescriptor):
                fields.append(nam)
        return fields

    def _get_models(self):
        """
        Берем все модели, в которых есть FileField
        :return: список классов моделей
        """
        models = {}

        is_model = lambda x: (
            inspect.isclass(x) and
            isinstance(x, ModelBase) and
            not x._meta.abstract
        )

        apps = settings.INSTALLED_APPS
        for app in apps:
            try:
                models_module = import_module('{0}.models'.format(app))
            except ImportError:
                continue
            for name, cls in inspect.getmembers(models_module):
                if is_model(cls) and cls not in models:
                    fields = self._get_fields(cls)
                    if fields:
                        models[cls] = fields

        return models

    def _delete_all_files(self, models):
        """
        Сервисный метод. Используется для технических нужд.
        В работе команды не учавствует.
        """
        for model, fields in six.iteritems(models):
            kwargs = dict(list(zip(fields, ['']*len(fields))))
            cnt = model.objects.all().update(**kwargs)
            print(u'{0}: {1}'.format(model, cnt))

    def _send_file(self, file_name):
        """
        Непосредственная отправка файла на ATCFS.
        :param file_name: название файла
        :return: идентификатор файла в ATCFS
        """
        ident = u''
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        try:
            with open(file_path, 'r') as fd:
                ident = self.api.upload_file(
                    os.path.basename(file_name), fd.read()
                )
        except IOError:
            pass
        return ident

    def _get_objs(self, model, fields):
        """
        Запрашиваем из базы напрямую объекты по модели.
        :param model: класс модели
        :param fields: список полей
        :return: список словарей в которых id и значения полей
        """
        cursor = connection.cursor()
        select_fields = u', '.join(fields)
        where_fields = u' OR '.join(
            [u'COALESCE({0}, \'\') <> \'\''.format(field) for field in fields]
        )
        sql = u'SELECT id, {0} from {1} WHERE {2};'.format(
            select_fields,
            model._meta.db_table,
            where_fields
        )
        cursor.execute(sql)
        objs = dictfetchall(cursor)
        return objs

    def _update_objs(self, model, objs):
        """
        Изменяем значения полей в базе.
        :param model: класс модели
        :param objs: словарь списков, где ключ - id объекта,
        а значение - список тюплов (название, значение)
        """
        cursor = connection.cursor()
        sql = u''
        for obj_id, obj_fields in six.iteritems(objs):
            set_fields = u', '.join(
                [u'{0[0]} = \'{0[1]}\''.format(field) for field in obj_fields]
            )
            sql += u'UPDATE {0} SET {1} WHERE id = {2};'.format(
                model._meta.db_table,
                set_fields,
                obj_id
            )
        if sql:
            cursor.execute(sql)
            commit_unless_managed()

    def _migrate_all_files(self, models):
        """
        Проходимся по всем моделям, всем объектам, отсылаем файлы на ATCFS.
        :param models: модели, в которых есть FileField
        """
        total = len(models)
        for i, (model, fields) in enumerate(six.iteritems(models), start=1):
            print(self.style.SQL_KEYWORD(
                u'{0} ({1}/{2})'.format(model, i, total)
            ))
            objs = self._get_objs(model, fields)
            updated_objs = {}
            for obj in objs:
                updated_fields = []
                for field_name in fields:
                    field_value = obj[field_name]
                    if field_value:
                        ident = self._send_file(field_value)
                        updated_fields.append((field_name, ident))
                        print(u'{0},{1},{2},{3}'.format(
                            obj['id'],
                            field_name.decode('UTF-8'),
                            field_value.decode('UTF-8'),
                            ident.decode('UTF-8')
                        ))
                updated_objs[obj['id']] = updated_fields
            self._update_objs(model, updated_objs)

    def handle_noargs(self, **options):
        models = self._get_models()
        if options['delete']:
            self._delete_all_files(models)
        else:
            self._migrate_all_files(models)
