# coding: utf-8


def lru_cache(**kwargs):
    """Замена декоратора lru_cache для Python до версии 3.2.

    Если lru_cache не может быть импортирован, то функция будет вызываться
    как обычно.

    :param kwargs: Параметры, которые нужно передать в lru_cache
    """
    try:
        from functools import lru_cache
    except ImportError:
        return lambda function: function
    else:
        return lru_cache(**kwargs)
