# coding: utf-8
u"""Данный модуль является IoC-контейнером.

Используется для связывания объектов и классов проекта с общей кодовой базой.
При необходимости использования в общей кодовой базе объектов проекта,
нужно добавить переменные со значением ``educommon.Undefined`` в данный модуль.
"""
from __future__ import absolute_import

from educommon import Undefined


observer = Undefined
u"""Реестр слушателей системы."""

main_controller = Undefined
u"""Контроллер, обеспечивающий работу с экшенами приложений."""

auth_controller = Undefined
u"""Контроллер, обеспечивающий работу с экшенами авторизации."""

roles_controller = Undefined
u"""Контроллер, обеспечивающий работу с экшенами реестра ролей RBAC."""

get_current_user = Undefined
u"""Функция для получения текущего пользователя, которому назначаются роли.

Должна реализовываться в проекте в связи с тем, что роли могут закрепляться за
любыми моделями проекта (пользователями, физ. лицами, сотрудниками, учениками,
родителями и т.д.).
"""

get_user_by_email = Undefined
u"""Функция, возвращающая учетную запись пользователя по его email'у."""

simple_auth__get_login_panel = Undefined
u"""Функция, возвращающая панель входа в систему в виде компонента."""

edureception__Specialist = Undefined
u"""Модель специалиста приема."""

edureception__Office = Undefined
u"""Модель кабинета."""

edureception__Applicant = Undefined
u"""Модель посетителя приема."""

edureception__TimeTableRecord = Undefined
u"""Модель специалиста приема."""

edureception__ApplicantReception = Undefined
u"""Модель кабинета."""

edureception__SpecialistCronTab = Undefined
u"""Модель посетителя приема."""

edureception__Organizations = Undefined
u"""Модель учереждений."""

edureception__Reasons = Undefined
u"""Модель причин записи на прием."""

edureception__IdentityDocumentsTypes = Undefined
u"""Модель типы документов, удостоверяющих личность."""


def has_value(name):
    u"""Возвращает True, если значение *name* было установлено.

    :param str name: Имя параметра в контейнере.

    :rtype: bool
    """
    return globals().get(name, Undefined) is not Undefined


def register(name, value):
    u"""Регистрирует в контейнере значение *value* под именем *name*.

    *name* должен быть объявлен в модуле и равен *Undefined*.
    """
    assert name in globals(), name

    # если в globals находится тоже самое значение,
    # то сразу возвращаем результат
    if globals()[name] is value:
        return value

    assert globals()[name] is Undefined, (
        u'"{}" already registered'.format(name)
    )

    globals()[name] = value

    return value


def get(name):
    u"""Возвращает содержимое с именем *name*.

    *name* должен быть предварительно зарегистрирован через **register**.
    """
    assert name in globals(), u'Object {} is not registered'.format(name)
    assert globals()[name] is not Undefined, (
        u'"{}" not registered'.format(name)
    )

    return globals()[name]
