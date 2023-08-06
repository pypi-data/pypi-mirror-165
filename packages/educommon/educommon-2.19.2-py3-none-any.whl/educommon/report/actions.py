# coding: utf-8
u"""Генерация отчётов средствами платформы M3."""
from __future__ import absolute_import

from m3 import ApplicationLogicException
from m3.actions import OperationResult
from objectpack.actions import BaseAction
from objectpack.actions import BasePack
from objectpack.actions import BaseWindowAction
from objectpack.ui import BaseEditWindow
import six


class BaseReportPack(BasePack):

    u"""Базовый класс отчёта.

    Отчёты на любых движках могут быть описаны на основе этого класса.
    """

    title = u'Отчёт'

    # дефолтное окно отчёта
    report_window = BaseEditWindow

    # признак асинхронного выполнения
    is_async = False

    # класс провайдера данных.
    data_provider_class = None

    # класс построителя отчётов
    report_builder_class = None

    # экземпляр класса провайдера
    data_provider = None

    # экземпляр класса построителя отчёта
    report_builder = None

    def create_provider(self, context):
        u"""Кастомный метод для создания экземпляра класса провайдера.

        Используется в случае необходимости явного вызова конструктора
        провайдера, например для композитного провайдера.

        Внимание! Экземпляр созданного провайдера должен быть присвоен
        атрибуту data_provider
        """

    def init_provider(self, context):
        u"""Кастомный метод для инициации провайдера.

        Данный метод должен извлечь параметры из контекста, а затем
        вызывать метод провайдера init().
        """

    def create_builder(self, context, *args, **kwargs):
        u"""Специальный метод для создания билдера.

        Извлекает параметры создания билдера из контекста или из *args/**kwargs
        затем инстанцирует билдер, присваивая его атрибуту self.report_builder
        """


def download_result(url):
    u"""функция для скачивания файла отчёта."""
    if not isinstance(url, six.text_type):
        url = six.text_type(url, 'utf-8')
    return OperationResult(
        success=True,
        code=u"""
            (function(){
                var hiddenIFrameID = 'hiddenDownloader',
                    iframe = document.getElementById(hiddenIFrameID);
                if (iframe === null) {
                    iframe = document.createElement('iframe');
                    iframe.id = hiddenIFrameID;
                    iframe.style.display = 'none';
                    document.body.appendChild(iframe);
                }
                iframe.src = "%s";
            })()
        """ % url
    )


class CommonReportWindowAction(BaseWindowAction):

    u"""Экшн показа окна параметров отчёта (перед выполнением отчёта)."""

    perm_code = 'report'

    def create_window(self):
        u"""создание окна параметров отчёта."""
        self.win = self.parent.create_report_window(self.request, self.context)

    def configure_window(self):
        u"""конфигурирование окна параметров отчёта."""
        self.win.save_btn.text = u'Сформировать'

    def set_window_params(self):
        u"""Задание параметров окна."""
        super(CommonReportWindowAction, self).set_window_params()
        params = self.win_params.copy()
        params['title'] = self.parent.title
        params['form_url'] = self.parent.get_reporting_url()
        self.win_params = self.parent.set_report_window_params(
            params, self.request, self.context)


class CommonReportAction(BaseAction):

    u"""Экшн, выполняющий отчёт."""

    perm_code = 'report'

    def run(self, request, context):
        u"""Выполнение запроса."""
        pack = self.parent
        # проверка параметров отчёта
        pack.check_report_params(request, context)
        provider_params = pack.get_provider_params(request, context)
        builder_params = pack.get_builder_params(request, context)

        if 'title' not in builder_params and hasattr(pack, 'title'):
            builder_params.update(title=pack.title)
        # генерация отчёта
        out_file_url = pack.make_report(provider_params, builder_params)
        return download_result(out_file_url.encode('utf-8'))


class CommonReportPack(BasePack):

    u"""
    Пак, реализующий генерацию отчётов.

    Использует класс-построитель reporter.
    """

    title = u'Отчёт'

    # дефолтное окно отчёта
    report_window = BaseEditWindow

    # признак асинхронного выполнения
    is_async = False

    reporter_class = None
    """
    класс построителя отчета, наследник SimpleReporter

    ..code:

        reporter = MySimpleReporter
    """

    def __init__(self):
        u"""Конструктор пака генерации отчётов."""
        super(CommonReportPack, self).__init__()

        self.report_window_action = CommonReportWindowAction()
        self.report_action = CommonReportAction()
        self.actions.extend([
            self.report_window_action,
            self.report_action,
        ])

    def get_reporting_url(self):
        u"""Отдаёт адрес форме, куда передавать данные для обработки."""
        return self.report_action.get_absolute_url()

    @staticmethod
    def context2dict(context):
        u"""преобразование контекста в словарь."""
        result = {}
        for key, value in six.iteritems(context.__dict__):
            try:
                if callable(value):
                    value = value()
                result[key] = value
            except TypeError:
                continue

        return result

    def check_report_params(self, request, context):
        u"""
        Проверка передаваемых параметров для формирования отчёта.

        :raise: ApplicationLogicException
        """
        pass

    def get_provider_params(self, request, context):
        u"""
        Преобразование request, context к словарю для создания провайдера.

        :param request:
        :param context:
        """
        return {}

    def get_builder_params(self, request, context):
        u"""
        Преобразование request, context к словарю для создания билдера.

        :param request:
        :param context:
        """
        return {}

    def init_reporter(self, provider_params, builder_params):
        u"""
        Инициализация построителя с передачей параметров билдеру и провайдеру.

        Не требует переопределения.
        """
        return self.reporter_class(provider_params, builder_params)

    def make_report(self, provider_params, builder_params):
        u"""Синхронное построение отчёта. Не требует переопределения."""
        reporter = self.init_reporter(provider_params, builder_params)
        url = reporter.make_report()
        return url

    def set_report_window_params(self, params, request, context):
        u"""Дополнение параметров окна отчёта."""
        if self.reporter_class.extension not in (
            self.reporter_class._available_extensions
        ):
            raise ApplicationLogicException(u'Расширение указано неверно!')
        params['extension'] = self.reporter_class.extension
        return params

    def create_report_window(self, request, context):
        u"""
        Cоздание окна настройки параметров отчёта.

        Не требует переопределения.
        """
        return self.report_window()

    def extend_menu(self, menu):
        u"""Размещение в меню."""
        pass
