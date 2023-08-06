# coding: utf-8
# pylint: disable=no-init
u"""Модели для хранения данных системы авторизации RBAC."""
from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db.models.signals import post_delete
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from m3 import ApplicationLogicException
from m3.db import safe_delete
from m3_django_compat import ModelOptions
from m3_django_compat import atomic
from m3_django_compat.models import GenericForeignKey
import six

from educommon.auth.rbac.utils import get_permission_full_title
from educommon.django.db.mixins.date_interval import ActualObjectsManager
from educommon.django.db.mixins.date_interval import DateIntervalMeta
from educommon.django.db.mixins.date_interval import DateIntervalMixin
from educommon.django.db.mixins.validation import post_clean
from educommon.django.db.models import BaseModel
from educommon.django.db.utils import model_modifier_metaclass
from educommon.m3.extensions.listeners.delete_check.mixins import \
    CascadeDeleteMixin

from . import config
from .permissions import PERM__ROLE__EDIT


@six.python_2_unicode_compatible
class Permission(BaseModel):

    u"""Разрешение."""

    name = models.CharField(
        u'Имя',
        max_length=100,
        db_index=True,
        unique=True,
    )
    title = models.CharField(
        u'Название',
        max_length=200,
        blank=True, null=True,
    )
    description = models.TextField(
        u'Описание',
        blank=True,
    )
    hidden = models.BooleanField(
        u'Видимость пользователям',
        default=False,
    )

    class Meta:
        verbose_name = u'Разрешение'
        verbose_name_plural = u'Разрешения'

    def __str__(self):
        return u'Permission<{}: {}>'.format(self.id, self.name)


@six.python_2_unicode_compatible
class Role(CascadeDeleteMixin, BaseModel):

    u"""Роль."""

    name = models.CharField(
        u'Название',
        max_length=300,
        db_index=True,
        unique=True,
    )
    description = models.TextField(
        u'Описание',
        blank=True,
    )
    can_be_assigned = models.BooleanField(
        u'Может быть назначена пользователю',
        default=True,
    )
    permissions = models.ManyToManyField(
        Permission,
        related_name='roles',
        through='RolePermission',
    )
    user_types = models.ManyToManyField(
        ContentType,
        verbose_name=u'Может быть назначена',
        through='RoleUserType',
        related_name='+',
    )

    class Meta:
        verbose_name = u'Роль'
        verbose_name_plural = u'Роли'

    def __str__(self):
        return u'Role<{}: {}>'.format(self.id, self.name)

    @property
    def subroles(self):
        u"""Возвращает все вложенные роли данной роли.

        :rtype: set
        """
        result = set()

        for role_parent in RoleParent.objects.filter(parent_id=self.id):
            result.add(role_parent.role)
            result.update(role_parent.role.subroles)

        return result

    def get_permissions(self):
        u"""Возвращает все разрешения роли, в т.ч. вложенных ролей.

        :rtype: QuerySet
        """
        roles = set([self]) | self.subroles
        result = Permission.objects.filter(
            pk__in=RolePermission.objects.filter(
                role__in=roles,
            ).values('permission'),
        )

        return result

    def simple_clean(self, errors):
        super(Role, self).simple_clean(errors)

        if (self.pk and not self.can_be_assigned and
                self.userrole_set.exists()):
            errors['can_be_assigned'].append(
                u'Есть пользователи, которым назначана роль "{}" '.format(
                    self.name
                )
            )

    def safe_delete(self):
        # safe_delete неправильно работает внутри транзакций, из-за этого
        # при вызове commit() валится IntegrityError, который надо обрабатывать
        # вручную.
        try:
            with atomic():
                # Удаление связей разрешений с ролью
                RolePermission.objects.filter(role=self).delete()

                # Удаление связей роли с родительскими ролями
                RoleParent.objects.filter(role=self).delete()

                # Удаление самой роли
                safe_delete(self)

            result = True
        except Exception as error:  # pylint: disable=broad-except
            if error.__class__.__name__ == 'IntegrityError':
                result = False
            else:
                raise

        return result


class RoleUserType(BaseModel):

    u"""M2M-модель "Тип пользователя роли"."""

    role = models.ForeignKey(
        Role,
        verbose_name=u'Роль',
        related_name='+',
        on_delete=models.CASCADE,
    )
    user_type = models.ForeignKey(
        ContentType,
        verbose_name=u'Тип пользователя',
        related_name='+',
        on_delete=models.CASCADE,
    )

    cascade_delete_for = (role,)
    display_related_error = False

    class Meta:
        unique_together = ('role', 'user_type')
        verbose_name = u'Тип пользователя роли'
        verbose_name_plural = u'Типы пользователей ролей'

    def simple_clean(self, errors):
        super(RoleUserType, self).simple_clean(errors)

        from educommon.auth.rbac.config import rbac_config

        if not self.role.can_be_assigned:
            errors['role'].append(
                u'Роль "{}" не может назначаться пользователям'.format(
                    self.role.name
                )
            )

        if (
            rbac_config.user_types and
            self.user_type.model_class() not in rbac_config.user_types
        ):
            errors['role'].append(
                u'Роль "{}" не может быть назначена типу "{}".'.format(
                    self.role.name,
                    self.user_type.name,
                )
            )

    @staticmethod
    def clean_role(instance, errors, **kwargs):
        u"""Проверяет типы пользователей роли при её изменении.

        Не допускает ситуаций, когда при отключении возможности назначения
        роли пользователям остаются ссылки на типы пользователей.

        Вызывается через сигнал ``post_clean`` модели
        :class:`~educommon.auth.rbac.models.Role`.

        :param instance: Роль.
        :type instance: :class:`~educommon.auth.rbac.models.Role`

        :param errors: Словарь с сообщениями об ошибках валидации.
        :type errors: :class:`defaultdict`
        """
        if instance.can_be_assigned:
            return

        if instance.user_types.exists():
            errors[NON_FIELD_ERRORS].append(
                u'Для снятия флага "Может быть назначена пользователя", '
                u'необходимо отвязать все типы пользователей.'
            )


post_clean.connect(
    receiver=RoleUserType.clean_role,
    sender=Role,
    dispatch_uid='RoleUserType.clean_role'
)


class RolePermission(BaseModel):

    u"""M2M-модель "Разрешение роли"."""

    role = models.ForeignKey(
        Role,
        verbose_name=u'Роль',
        on_delete=models.CASCADE,
    )
    permission = models.ForeignKey(
        Permission,
        verbose_name=u'Разрешение',
        on_delete=models.CASCADE,
    )

    cascade_delete_for = (role,)
    display_related_error = False

    class Meta:
        verbose_name = u'Разрешение роли'
        verbose_name_plural = u'Разрешения ролей'
        unique_together = ('role', 'permission')
        db_table = 'rbac_role_permissions'

    def __str__(self):
        return 'Роль: {}; Разрешение: {}'.format(
            self.role.name, self.permission.title)


@receiver(pre_delete, sender=RolePermission)
def protect_role_edit_permission(instance, **kwargs):
    u"""Предотвращает удаление из всех ролей разрешение на редактирование роли.

    Если это разрешение удалить из всех ролей, то никто из пользователей больше
    не сможет внести изменения в реестр ролей.
    """
    if (
        not RolePermission.objects.filter(
            permission__name=PERM__ROLE__EDIT,
        ).exclude(
            id=instance.pk,
        ).exists() and
        instance.permission.name == PERM__ROLE__EDIT
    ):
        raise ApplicationLogicException(
            u'Роль "{role}" является единственной ролью в Cистеме, в которой '
            u'есть разрешение "{permission}". В системе должна оставаться '
            u'возможность настройки ролей, поэтому удаление из неё этого '
            u'разрешения невозможно. Для удаления разрешения "{permission}" '
            u'из роли "{role}" сначала назначьте данное разрешение любой '
            u'другой роли в системе.'
            .format(
                role=instance.role.name,
                permission=get_permission_full_title(instance.permission.name),
            )
        )


@six.python_2_unicode_compatible
class RoleParent(BaseModel):

    u"""M2M-модель "Вложенная роль"."""

    parent = models.ForeignKey(
        Role, related_name='+', on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        Role, related_name='+', on_delete=models.CASCADE
    )

    cascade_delete_for = (parent, role)
    display_related_error = False

    def simple_clean(self, errors):
        super(RoleParent, self).simple_clean(errors)

        if self.parent.id == self.role.id:
            errors['parent'].append(
                u'Роль не может содержать сама себя'
            )

        # ---------------------------------------------------------------------
        # Проверка отсутствия цикла
        query = RoleParent.objects.all()
        if self.pk:
            query = query.exclude(pk=self.pk)

        def check(target_role, role):
            for role_parent in query.filter(role=role):
                if target_role.id == role_parent.parent_id:
                    raise ValidationError(u'В иерархии ролей обнаружен цикл')
                check(target_role, role_parent.parent)

        try:
            # Проверка, нет ли self.role среди предков self.parent
            check(self.role, self.parent)
        except ValidationError as error:
            errors['parent'].extend(error.messages)
        # ---------------------------------------------------------------------

    def __str__(self):
        return u'RoleParent({} --> {})'.format(
            six.text_type(self.role), six.text_type(self.parent)
        )

    class Meta:
        unique_together = ('parent', 'role')
        verbose_name = u'Вложенная роль'
        verbose_name_plural = u'Вложенные роли'


UserRoleMeta = model_modifier_metaclass(
    DateIntervalMeta,
    date_from=dict(
        verbose_name=u'Действует с',
    ),
    date_to=dict(
        verbose_name=u'по',
    ),
)


@six.python_2_unicode_compatible
class UserRole(six.with_metaclass(UserRoleMeta, DateIntervalMixin, BaseModel)):

    u"""M2M-модель "Роль пользователя"."""

    no_intersections_for = ('content_type', 'object_id', 'role')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    user = GenericForeignKey()
    role = models.ForeignKey(
        Role,
        verbose_name=u'Роль',
        on_delete=models.CASCADE,
    )

    actual_objects = ActualObjectsManager()

    class Meta:
        verbose_name = u'Роль пользователя'
        verbose_name_plural = u'Роли пользователя'

    def __str__(self):
        return u'UserRole({} --> {})'.format(
            six.text_type(self.user), six.text_type(self.role),
        )

    def interval_intersected_error_message(self, others=None):
        return (
            u'Роль "{}" уже назначена этому пользователю в указанном '
            u'интервале дат.'.format(self.role.name)
        )

    def simple_clean(self, errors):
        super(UserRole, self).simple_clean(errors)

        if not self.role.can_be_assigned:
            errors['role'].append(
                u'Роль "{}" не может быть назначена пользователю'.format(
                    self.role.name
                )
            )

        if (
            config.rbac_config.user_types and
            self.role_id and
            self.content_type_id and
            not RoleUserType.objects.filter(
                role_id=self.role_id,
                user_type_id=self.content_type_id,
            ).exists()
        ):
            errors['role'].append(
                u'Роль "{}" не доступна для назначения '
                u'пользователям типа "{}".'.format(
                    self.role.name,
                    self.content_type.name,
                )
            )


@receiver(post_delete)
def delete_user_roles(instance, **kwargs):  # pylint: disable=unused-argument
    u"""Удаление привязки ролей к пользователям при удалении пользователя."""
    # Если модель была удалена из Системы, то при накатывании миграций, в
    # которых удаляются записи таких моделей случается AttributeError.
    try:
        content_type = ContentType.objects.get_for_model(instance)
    except AttributeError:
        return

    if content_type is None:
        return

    opts = ModelOptions(instance)
    try:
        opts.get_field_by_name('id')
    except FieldDoesNotExist:
        return

    UserRole.objects.filter(
        content_type=content_type,
        object_id=instance.id,
    ).delete()
