# coding: utf-8
from __future__ import absolute_import

from copy import deepcopy
from inspect import isclass
from weakref import WeakKeyDictionary
import warnings

from django.core.validators import MaxLengthValidator
from django.db.models.base import ModelBase
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from m3_django_compat import ModelOptions
from m3_django_compat import atomic
from m3_django_compat import get_model
import django
import six


# Кэш оригинальных объектов
_original_objects_cache = WeakKeyDictionary()


def model_modifier_metaclass(meta_base=ModelBase, **params):
    u"""Возвращает метакласс, изменяющий параметры полей модели.

    :param dict params: Словарь с новыми значениями параметров полей. Ключ
        словаря должен содержать имя поля в модели (*field.attname*), а
        значение - словарь с новыми параметрами поля.

    .. note::

       Пример использования:

       .. code::

          class BaseModel(models.Model):
              name = models.CharField(max_length=150)

          modified_model_params = {
              'name': {
                  'max_length': 300
              }
          }
          class MyModel(BaseModel):
              # Модель с увеличенной до 300 символов длиной поля name.
              __metaclass__ = model_modifier_metaclass(**modified_model_params)

              class Meta:
                  verbose_name = u'Образец справочника'
    """
    class ModifiedModelBase(meta_base):
        def __new__(cls, name, bases, attrs):
            model = super(ModifiedModelBase, cls).__new__(
                cls, name, bases, attrs
            )

            # Переопределения имен атрибутов (см. Field.deconstruct).
            attr_overrides = {
                'unique': '_unique',
                'error_messages': '_error_messages',
                'validators': '_validators',
                'verbose_name': '_verbose_name',
            }
            opts = ModelOptions(model)
            for field_name, field_params in six.iteritems(params):
                field = opts.get_field(field_name)
                for param_name, param_value in six.iteritems(field_params):
                    assert hasattr(field, param_name), param_name
                    setattr(field, param_name, param_value)
                    if param_name in attr_overrides:
                        setattr(field, attr_overrides[param_name], param_value)

                if 'max_length' in field_params:
                    field.validators = deepcopy(field.validators)
                    for validator in field.validators:
                        if isinstance(validator, MaxLengthValidator):
                            validator.limit_value = field_params['max_length']

            return model

    return ModifiedModelBase


def nested_commit_on_success(func):
    u"""Аналог commit_on_success, не завершающий существующую транзакцию.

    .. deprecated:: 0.16

       Используйте :func:`m3_django_compat.atomic`.
    """
    warnings.warn('Use m3_django_compat.atomic instead', DeprecationWarning)

    return atomic(func, savepoint=False)


def get_original_object(obj):
    u"""Возвращает загруженный из БД объект модели.

    Если первичный ключ не заполнен, либо в БД нет такого объекта, то
    возвращает None.
    """
    if obj.pk is None:
        result = None
    elif obj in _original_objects_cache:
        result = _original_objects_cache[obj]
    else:
        try:
            result = obj.__class__.objects.get(pk=obj.pk)

        except obj.__class__.DoesNotExist:
            result = None

        _original_objects_cache[obj] = result

    return result


@receiver(post_delete)
@receiver(post_save)
def _clear_cache(instance, **kwargs):
    u"""Удаляет объект из кэша функции ``get_original_object``."""
    if instance in _original_objects_cache:
        del _original_objects_cache[instance]


class LazyModel(object):

    u"""Класс для отложенной загрузки моделей.

    Предоставляет указывать в аргументах методов модель различными способами и
    единообразно получать доступ к модели. При этом модель может быть указана
    как строка, кортеж или класс модели.

    .. hint::

       Указание моделей в виде строк и кортежей актуально, когда есть
       потребность избежать прямого импорта моделей. Например, в коде, который
       выполняется до инициализации приложений Django ORM.

    .. code-block:: python
       :caption: Пример использования

       class ModelProcessor(object):
           def __init__(self, model):
               self._model = LazyModel(model)

           @property
           def model(self):
               return self._model.get_model()

       mp1 = ModelProcessor('person.Person')
       mp2 = ModelProcessor(('person', 'Person'))
       mp3 = ModelProcessor(Person)
    """

    def __init__(self, model):
        if (
            isinstance(model, six.string_types) and
            '.' in model and model.index('.') == model.rindex('.')
        ):
            self.app_label, self.model_name = model.split('.')
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        elif (
            isinstance(model, tuple) and
            len(model) == 2 and
            all(isinstance(s, six.string_types) for s in model)
        ):
            self.app_label, self.model_name = model
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        elif (
            isclass(model) and
            hasattr(model, '_meta') and
            hasattr(model._meta, 'app_label') and
            hasattr(model._meta, 'model_name')
        ):
            self._model = model
            self.app_label = model._meta.app_label
            self.model_name = model.__name__
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        else:
            raise ValueError(
                '"model" argument has invalid value: ' + repr(model)
            )

    def get_model(self):
        u"""Возвращает класс модели, заданной при инициализации."""
        if not hasattr(self, '_model'):
            self._model = get_model(self.app_label, self.model_name)

        return self._model


if django.VERSION >= (1, 8):
    from django.db.models.expressions import Func
    from django.db.models.lookups import Lookup

    class SmartExact(Func):

        u"""Удаляет пробелы из строки и заменяет буквы ё на е."""

        template = u"TRANSLATE(%(expressions)s, 'ёЁ ', 'еЕ')"

    class SmartExactLookup(Lookup):

        u"""Удаляет пробелы из строки и заменяет буквы ё на е."""

        lookup_name = 'smart_exact'

        def as_postgresql(self, compiler, connection):
            lhs, lhs_params = self.process_lhs(compiler, connection)
            rhs, rhs_params = self.process_rhs(compiler, connection)

            sql = u"TRANSLATE(%s, 'ёЁ ', 'еЕ')"
            sql = u'{sql} = {sql}'.format(sql=sql)

            return sql % (lhs, rhs), lhs_params + rhs_params

    class SmartIExact(Func):

        u"""Переводит в верхний регистр, удаляет пробелы, заменяет Ё на Е."""

        template = u"TRANSLATE(UPPER(%(expressions)s), 'Ё ', 'Е')"

    class SmartIExactLookup(Lookup):

        u"""Переводит в верхний регистр, удаляет пробелы, заменяет Ё на Е."""

        lookup_name = 'smart_iexact'

        def as_postgresql(self, compiler, connection):
            lhs, lhs_params = self.process_lhs(compiler, connection)
            rhs, rhs_params = self.process_rhs(compiler, connection)

            sql = u"TRANSLATE(UPPER(%s), 'Ё ', 'Е')"
            sql = u'{sql} = {sql}'.format(sql=sql)

            return sql % (lhs, rhs), lhs_params + rhs_params

    class SmartIContainsLookup(Lookup):

        u"""
        Переводит в верхний регистр, удаляет пробелы, заменяет Ё на Е,
        проверяет вхождение текста.
        """

        lookup_name = 'smart_icontains'

        def as_postgresql(self, compiler, connection):
            lhs, lhs_params = self.process_lhs(compiler, connection)
            rhs, rhs_params = self.process_rhs(compiler, connection)

            sql = u"TRANSLATE(UPPER(%s), 'Ё ', 'Е')"
            sql = u"{sql} like '%%%%' || {sql} || '%%%%'".format(sql=sql)

            return sql % (lhs, rhs), lhs_params + rhs_params
