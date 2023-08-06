# coding: utf-8
from __future__ import absolute_import

from functools import partial
import re

from django.core.validators import RegexValidator

from educommon.django.db.validators.simple import validate_value


package_name_validator = RegexValidator(re.compile(
    r'(^[_a-z][_a-z0-9]*$)|(^[_a-z][._a-z0-9]*[_a-z0-9]{1}$)', re.IGNORECASE
))
u"""Валидатор имени пакета."""

is_package_name_valid = partial(validate_value,
                                validator=package_name_validator)
