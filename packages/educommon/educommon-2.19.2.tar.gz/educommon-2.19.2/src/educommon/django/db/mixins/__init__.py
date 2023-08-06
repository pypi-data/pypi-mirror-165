# coding: utf-8
u"""Классы-примеси для моделей Django."""
from __future__ import absolute_import

from django.db import models
from m3_django_compat import atomic
import six


class DeferredActionsMixin(models.Model):

    """Класс-примесь для выполнения отложенных действий в моделях.

    Позволяет выполнять действия, оформленные в виде callable-объектов,
    до/после сохранения/удаления объекта модели.

    .. code-block:: python

       class TestModel(DeferredActionsMixin, BaseModel):
           def simple_clean(self, errors):
               super(TestModel, self).simple_clean()

               if self.status_id != get_original_object(self).status_id:
                   log = Log.objects.create(
                       object_id=self.id,
                   )
                   log.full_clean()
                   self.after_save(log.save)
    """

    class Meta:  # noqa: D106
        abstract = True

    def __init__(self, *args, **kwargs):  # noqa: D107
        super(DeferredActionsMixin, self).__init__(*args, **kwargs)

        self.__pre_save_actions = []
        self.__post_save_actions = []
        self.__pre_delete_actions = []
        self.__post_delete_actions = []

    def before_save(self, action):
        """Добавляет действие, которое будет выполнено ДО сохранения."""
        self.__pre_save_actions.append(action)

    def after_save(self, action):
        """Добавляет действие, которое будет выполнено ПОСЛЕ сохранения."""
        self.__post_save_actions.append(action)

    def before_delete(self, action):
        """Добавляет действие, которое будет выполнено ДО удаления."""
        self.__pre_delete_actions.append(action)

    def after_delete(self, action):
        """Добавляет действие, которое будет выполнено ПОСЛЕ удаления."""
        self.__post_delete_actions.append(action)

    def __execute_actions(self, actions):
        """Выполняет запланированные ранее действия."""
        while actions:
            action = actions.pop()
            action()

    @atomic
    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Дополняет сохранение объекта выполнением запланированных действий.

        Действия, выполняемые **до** и **после** сохранения добавляются с
        помощью методов :meth:`before_save` и :meth:`after_save`
        соответственно.
        """
        self.__execute_actions(self.__pre_save_actions)
        super(DeferredActionsMixin, self).save(*args, **kwargs)
        self.__execute_actions(self.__post_save_actions)

    @atomic
    def delete(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Дополняет удаление объекта выполнением запланированных действий.

        Действия, выполняемые **до** и **после** удаления добавляются с
        помощью методов :meth:`before_delete` и :meth:`after_delete`
        соответственно.
        """
        self.__execute_actions(self.__pre_delete_actions)
        result = super(DeferredActionsMixin, self).delete(*args, **kwargs)
        self.__execute_actions(self.__post_delete_actions)
        return result

    @atomic
    def safe_delete(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Дополняет удаление объекта выполнением запланированных действий.

        Действия, выполняемые **до** и **после** удаления добавляются с
        помощью методов :meth:`before_delete` и :meth:`after_delete`
        соответственно.
        """
        self.__execute_actions(self.__pre_delete_actions)
        result = super(DeferredActionsMixin, self).safe_delete(*args, **kwargs)
        self.__execute_actions(self.__post_delete_actions)
        return result


class DeleteOnSaveMixin(models.Model):

    u"""Примесь для удаления объектов до/после сохранения модели.

    Функционал данной примеси актуален при валидации моделей. В некоторых
    случаях во время валидации выясняется, что какой-либо зависимый объект
    должен быть удален. Но т.к. во время валидации экземляра модели удалять
    объект еще рано, то можно этот объект пометить для удаления до/после
    сохранения экземпляра модели.

    Рекомендуется указывать данную примесь первой в списке базовых классов
    модели, тогда удаление объектов будет выполняться в первую/последнюю
    очередь.
    """

    def __init__(self, *args, **kwargs):
        super(DeleteOnSaveMixin, self).__init__(*args, **kwargs)

        # Список объектов, подлежащих удалению после сохранения self
        self.__objects_for_delete_before_save = set()
        self.__objects_for_delete_after_save = set()

    def delete_before_save(self, obj):
        u"""Добавляет объект в список удаляемых **перед** сохранением.

        Указанный в аргументе `obj` объект помещается в список объектов,
        которые будут удалены **до** сохранения.

        :param obj: Объект модели, подлежащий удалению **до** сохранения.
        :type obj: django.db.models.Model
        """
        if obj is None:
            return

        assert isinstance(obj, models.Model), type(obj)

        if obj not in self.__objects_for_delete_after_save:
            self.__objects_for_delete_before_save.add(obj)

    def delete_after_save(self, obj):
        u"""Добавляет объект в список удаляемых **после** сохранения.

        Указанный в аргументе `obj` объект помещается в список объектов,
        которые будут удалены **после** сохранения.

        :param obj: Объект модели, подлежащий удалению **после** сохранения.
        :type obj: django.db.models.Model
        """
        if obj is None:
            return

        assert isinstance(obj, models.Model), type(obj)

        if obj not in self.__objects_for_delete_before_save:
            self.__objects_for_delete_after_save.add(obj)

    @atomic
    def save(self, *args, **kwargs):
        def delete_object(obj):
            if hasattr(obj, 'safe_delete'):
                obj.safe_delete()
            else:
                obj.delete()

        def delete_objects(objects):
            while objects:
                obj = objects.pop()
                if obj.pk is not None and obj != self:
                    delete_object(obj)

        delete_objects(self.__objects_for_delete_before_save)

        super(DeleteOnSaveMixin, self).save(*args, **kwargs)

        delete_objects(self.__objects_for_delete_after_save)

    class Meta:
        abstract = True


class StringFieldsCleanerMixin(models.Model):

    u"""Примесь для удаления из строковых полей модели лишних пробелов.

    Во всех текстовых полях модели удаляет пробельные символы в начале и конце
    строки, несколько идущих подряд пробелов заменяет на один.

    Для полей с разрешенными пустыми значениями (null=True) пустые строки
    заменяет на None.

    .. note::
       В документации Django текстовых полей не рекомендуется использовать
       значение *None*, т.к. в этом случае возникает неоднозначность - пустым
       значением будет являться не только None, но и пустая строка. Подробнее
       см. http://djbook.ru/rel1.4/ref/models/fields.html#null. Но
       использование пустой строки совместно с ограничением уникальности
       приводит к невозможности сохранения более одной записи с пустым
       значением, поэтому для однозначности в текстовых полях будем
       использовать значение None, если указано null=True, и пустую строку в
       остальных случаях.
    """

    def clean_fields(self, exclude=None):
        for field in self._meta.fields:
            if isinstance(field, (models.TextField, models.CharField)):
                field_value = getattr(self, field.attname)

                if field_value is not None:
                    field_value = six.text_type(field_value).strip()
                    # Удаление лишних пробелов
                    while field_value.find(u'  ') != -1:
                        field_value = field_value.replace(u'  ', u' ')

                if not field_value:
                    field_value = None if field.null else u''

                setattr(self, field.attname, field_value)

        return super(StringFieldsCleanerMixin, self).clean_fields(exclude)

    class Meta:
        abstract = True
