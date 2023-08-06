# coding: utf-8
from __future__ import absolute_import

from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic import TemplateView


def register_urlpatterns():
    urlpatterns = patterns('',
        url(
            r'^atcfs_unavailable/$',
            TemplateView.as_view(template_name='atcfs_unavailable.html'),
            name='atcfs_unavailable'
        ),
    )
    return urlpatterns
