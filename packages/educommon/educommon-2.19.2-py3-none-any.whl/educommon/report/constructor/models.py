# coding: utf-8
from __future__ import absolute_import

from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from objectpack.exceptions import ValidationError

from educommon.django.db.mixins.validation import post_clean
from educommon.django.db.models import BaseModel
from educommon.m3.extensions.listeners.delete_check.mixins import \
    CascadeDeleteMixin
from educommon.utils.misc import cached_property

from . import constants
from .registries import registry
from .validators import validate_data_source_name


# -----------------------------------------------------------------------------
class ReportTemplate(CascadeDeleteMixin, BaseModel):

    u"""Модель "Шаблон отчета"."""

    USER_DEFINED = constants.FORMAT_USER_DEFINED
    EXCEL_SIMPLE = constants.FORMAT_EXCEL_SIMPLE
    EXCEL_MERGED = constants.FORMAT_EXCEL_MERGED
    FORMAT_CHOICES = constants.FORMAT_CHOICES

    title = models.CharField(
        u'Наименование шаблона отчета',
        max_length=1000,
        unique=True,
    )
    data_source_name = models.CharField(
        u'Имя источника данных',
        max_length=500,
        validators=[validate_data_source_name],
    )
    format = models.PositiveSmallIntegerField(
        u'Формат сборки',
        choices=FORMAT_CHOICES,
        default=USER_DEFINED,
    )
    include_available_units = models.BooleanField(
        u'Отображать данные по дочерним организациям', default=False
    )

    class Meta:
        verbose_name = u'Отчет'
        verbose_name_plural = u'Отчеты'

    def simple_clean(self, errors):
        # ---------------------------------------------------------------------
        # Проверка уникальности наименования шаблона отчета.
        if self.title:
            query = ReportTemplate.objects.filter(
                title__smart_iexact=self.title,
            )
            if self.pk:
                query = query.exclude(pk=self.pk)

            if query.exists():
                errors['title'].append(
                    u'Шаблон отчета с подобным именем уже существует.'
                )
        # ---------------------------------------------------------------------
        super(ReportTemplate, self).simple_clean(errors)

    @cached_property
    def data_source(self):
        if self.data_source_name not in registry:
            raise ValidationError(
                u'В шаблоне отчета указан несуществующий источник данных ({}).'
                .format(self.data_source_name)
            )
        data_source = registry.get(
            self.data_source_name
        ).get_data_source_descriptor()
        return data_source

    def __str__(self):
        return 'Шаблон отчета: {}'.format(self.title)
# -----------------------------------------------------------------------------


class ReportColumn(BaseModel):

    u"""Модель "Столбец отчета"."""

    # Направления сортировки.
    ASCENDING = constants.SORT_ASCENDING
    DESCENDING = constants.SORT_DESCENDING
    SORT_CHOICES = constants.SORT_CHOICES

    report_template = models.ForeignKey(
        ReportTemplate,
        verbose_name=u'Отчет',
        related_name='columns',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        u'Имя столбца в источнике данных',
        max_length=300,
    )
    index = models.PositiveSmallIntegerField(
        u'Порядковый номер',
    )
    visible = models.BooleanField(
        u'Видимость колонки в отчете',
        default=True,
    )
    title = models.CharField(
        u'Отображаемое имя',
        max_length=300,
        null=True, blank=True,
    )
    by_value = models.PositiveSmallIntegerField(
        u'Промежуточный итог',
        choices=constants.BY_VALUE_CHOICES,
        blank=True,
        null=True
    )
    total = models.PositiveSmallIntegerField(
        u'Итог',
        choices=constants.TOTAL_CHOICES,
        blank=True,
        null=True
    )

    cascade_delete_for = (report_template,)

    class Meta:
        verbose_name = u'Столбец отчета'
        verbose_name_plural = u'Столбцы отчетов'
        unique_together = (
            ('report_template', 'name'),
        )
        ordering = (
            'index',
        )

    def _clean_aggregator_type(self, errors):
        u"""Проверяет на соответствие типов итогов."""
        if not (
            (self.by_value == self.total) or
            (any(not bool(item) for item in (self.by_value, self.total)))
        ):
            errors['by_value'].append(
                u'Тип для "Промежуточный итог" и "Итог" должен совпадать.'
            )

    def _clean_aggregator_data_type(self, errors):
        u"""Проверяет тип данных для итогов."""
        # Определяем тип данных в колонке.
        data_source_descriptor = registry.get(
            self.report_template.data_source_name
        ).get_data_source_descriptor()
        column_descriptor = data_source_descriptor.get_column_descriptor(
            self.name
        )
        is_num_data_type = column_descriptor.data_type == constants.CT_NUMBER
        # Определяем тип Промежуточного итога.
        is_sum_by_value = (
            self.by_value and self.by_value == constants.BY_VALUE_SUM
        )
        # Определяем тип Итога.
        is_total_sum = self.total and self.total == constants.TOTAL_SUM
        aggregator_info = (
            ('by_value', is_sum_by_value),
            ('total', is_total_sum)
        )
        for aggregator_type, is_sum in aggregator_info:
            if is_sum and not is_num_data_type:
                errors[aggregator_type].append(
                    u'Подсчет суммы недопустим для колонки "{}".'.format(
                        column_descriptor.get_full_title(),
                    )
                )

    def simple_clean(self, errors):
        u"""Добавляет проверку для подсчета итогов."""
        self._clean_aggregator_type(errors)
        self._clean_aggregator_data_type(errors)

        super(ReportColumn, self).simple_clean(errors)

    def __str__(self):
        return self.title
# -----------------------------------------------------------------------------


class ReportFilterGroup(MPTTModel, BaseModel):

    u"""Группа фильтров.

    Фильтры объединяются в группы с помощью логических операторов "И" и "ИЛИ".
    При этом группы фильтров также могут быть объединены в группы. В итоге
    получается древовидная структура, представляющая собой подобие
    синтаксического дерева. Модели ``ReportFilterGroup`` и ``ReportFilter``
    используются для формирования таких деревьев.
    """

    # В связи с временными ограничениями на разработку функционала в окне
    # редактирования шаблона отображается "плоский" список фильтров, а не
    # древовидная иерархия. В связи с этим, несмотря на наличие возможности
    # хранить в БД сложно организованные фильтры, в интерфейсе такой
    # возможности не предусматрено. В случае, если у пользователей в будущем
    # возникнет потребность в создании более сложных фильтров, понадобится
    # переработка только интерфейсной части (окна редактирования шаблона).

    OPERATOR_AND = 1
    OPERATOR_OR = 2
    OPERATOR_CHOICES = (
        (OPERATOR_AND, u'И'),
        (OPERATOR_OR, u'ИЛИ'),
    )

    report_template = models.ForeignKey(
        ReportTemplate,
        verbose_name=u'Отчет',
        related_name='filter_groups',
        on_delete=models.CASCADE,
    )
    parent = TreeForeignKey(
        'self',
        blank=True, null=True,
        verbose_name=u'Родительская группа',
        related_name='nested_groups',
        on_delete=models.CASCADE,
    )
    operator = models.PositiveSmallIntegerField(
        u'Логический оператор',
        help_text=u'Логический оператор, объединяющий фильтры в группе',
        choices=OPERATOR_CHOICES,
    )

    cascade_delete_for = (report_template,)

    class Meta:
        verbose_name = u'Группа фильтров'
        verbose_name_plural = u'Группы фильтров'

    def __str__(self):
        return self.get_operator_display()

    @staticmethod
    def check_filter(instance, errors, **kwargs):
        u"""Проверка фильтров в контексте группы фильтров.

            1. Группа фильтра и столбца фильтра должны быть в одном и том же
               шаблоне.

        Вызывается через сигнал ``post_clean`` для объектов модели
        ``ReportFilter``.

        :param instance: Проверяемый период обучения.
        :type instance: :class:`~extedu.core.models.period.Period`

        :param errors: Словарь с сообщениями об ошибках валидации.
        :type errors: :class:`defaultdict`
        """
        report_filter = instance

        if (
            not report_filter.pk or
            not report_filter.group_id or
            not report_filter.column_id or
            not report_filter.group.report_template_id
        ):
            return

        column = report_filter.column
        group = report_filter.group
        # ---------------------------------------------------------------------
        # Колонка фильтра должна быть в том же шаблоне, что и группа.

        if column.report_template_id != group.report_template_id:
            errors['column'].append(
                u'Шаблон, к которому относится столбец фильтра "{}" '
                u'отличается от шаблона, к которому относится группа фильтров.'
                .format(column.name)
            )
        # ---------------------------------------------------------------------

    def simple_clean(self, errors):
        super(ReportFilterGroup, self).simple_clean(errors)
        # ---------------------------------------------------------------------
        # Все столбцы в фильтрах группы должны быть в том же шаблоне, что и
        # данная группа.

        if (
            self.pk and
            self.report_template_id and
            self.filters.exclude(
                column__report_template=self.report_template_id,
            ).exists()
        ):
            errors['report_template'].append(
                u'В данной группе есть фильтры, ссылающиеся на столбцы из '
                u'другого шаблона.'
            )
        # ---------------------------------------------------------------------
        # Шаблоны данной группы и родительской должны совпадать.

        if (
            self.pk and self.report_template_id and
            self.parent and self.parent.report_template_id and
            self.report_template_id != self.parent.report_template_id
        ):
            errors['parent'].append(
                u'Шаблон данной группы фильтров ("{}") отличается от шаблона '
                u'родительской группы ("{}").'.format(
                    self.report_template.title,
                    self.parent.report_template.title,
                )
            )
# -----------------------------------------------------------------------------


class ReportFilter(BaseModel):

    u"""Модель "Параметр фильтрации данных отчета"."""

    group = models.ForeignKey(
        ReportFilterGroup,
        verbose_name=u'Группа фильтров',
        related_name='filters',
        on_delete=models.CASCADE,
    )
    column = models.ForeignKey(
        ReportColumn,
        verbose_name=u'Столбец',
        related_name='filters',
        on_delete=models.CASCADE,
    )
    index = models.PositiveSmallIntegerField(
        u'Порядковый номер',
    )
    operator = models.PositiveSmallIntegerField(
        u'Оператор сравнения',
        choices=constants.OPERATOR_CHOICES,
    )
    exclude = models.BooleanField(
        u'Исключать записи, удовлетворяющие условию',
        default=False,
    )
    case_sensitive = models.NullBooleanField(
        u'Учет регистра',
    )
    values = ArrayField(
        models.TextField(
            u'Значение',
            blank=True, null=True,
        ),
        blank=True, null=True,
    )
    comment = models.TextField(
        u'Описание фильтра',
        blank=True, null=True,
    )

    cascade_delete_for = (group, column)

    def __str__(self):
        """Возвращает строку вида:
        `Поле "<название_поля>" [не ]<оператор:меньше или равно|меньше|...>
        "<значение>", <без учета|с учетом> регистра`
        :return:
        """
        template = (
            u'Поле "{col}"{invert__op:10}{operator} '
            u'"{value}", {case} регистра'
        )
        invert__op = u' не ' if self.exclude else u' '
        case = u'с учетом' if self.case_sensitive else u'без учета'
        return template.format(col=self.column, invert__op=invert__op,
                               operator=self.get_operator_display().lower(),
                               value=u', '.join(self.values), case=case)

    class Meta:
        verbose_name = u'Фильтр'
        verbose_name_plural = u'Фильтры'
        unique_together = (
            ('column', 'index'),
        )
        ordering = (
            'index',
        )

    def simple_clean(self, errors):
        super(ReportFilter, self).simple_clean(errors)
        # ---------------------------------------------------------------------
        # Значение должно быть указано для всех операторов, кроме IS_NULL.

        if self.operator == constants.IS_NULL:
            self.values = None

        elif (
            self.operator == constants.BETWEEN and
            (
                not self.values or
                len(self.values) != 2
            )
        ):
            errors['values'].append(
                u'Для оператора "{}" должно быть указано два значения.'
                .format(self.get_operator_display())
            )

        elif (
            self.operator not in (constants.IN, constants.BETWEEN,) and
            (
                not self.values or
                len(self.values) > 1
            )
        ):
            errors['values'].append(
                u'Должно быть указано только одно значение.'
            )

        elif not self.values:
            errors['values'].append(u'Не указано значение для сравнения.')
        # ---------------------------------------------------------------------

        if (
            self.group and self.column and
            self.group.report_template_id != self.column.report_template_id
        ):
            errors['column'].append(
                u'Группа и колонка принадлежат разным шаблонам.'
            )
        # ---------------------------------------------------------------------

        data_source_descriptor = registry.get(
            self.group.report_template.data_source_name
        ).get_data_source_descriptor()
        column_descriptor = data_source_descriptor.get_column_descriptor(
            self.column.name
        )
        data_type = column_descriptor.data_type
        valid_operators = constants.VALID_OPERATORS[data_type]
        if self.operator and self.operator not in valid_operators:
            errors['operator'].append(
                u'Оператор "{}" недопустим для колонки "{}".'.format(
                    self.get_operator_display(),
                    column_descriptor.get_full_title(),
                )
            )
# -----------------------------------------------------------------------------


class ReportSorting(BaseModel):

    u"""Модель "Параметр сортировки данных отчета"."""

    column = models.OneToOneField(
        ReportColumn,
        verbose_name=u'Колонка',
        related_name='sorting',
        on_delete=models.CASCADE,
    )
    direction = models.PositiveSmallIntegerField(
        u'Направление сортировки',
        choices=constants.DIRECTION_CHOICES,
    )
    index = models.PositiveSmallIntegerField(
        u'Порядковый номер',
    )

    class Meta:
        verbose_name = u'Сортировка'
        verbose_name_plural = u'Сортировка'
        ordering = ('index',)

    def __str__(self):
        return u'{col} ({direction})'.format(
            col=self.column, direction=self.get_direction_display().lower()
        )
# -----------------------------------------------------------------------------


post_clean.connect(ReportFilterGroup.check_filter, ReportFilter,
                   dispatch_uid='ReportFilterGroup.check_filter')
