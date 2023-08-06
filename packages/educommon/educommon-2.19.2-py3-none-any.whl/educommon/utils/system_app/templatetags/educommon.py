# coding: utf-8
from __future__ import absolute_import

import json

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def jsonify(obj):
    u"""Преобразование объкта в JSON."""
    return mark_safe(json.dumps(obj))
