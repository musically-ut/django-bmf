#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
This is a normal urlconf. it is imported from djangobmf.sites.site.get_url, where
the module views get appended by an '^module/' expression
"""

from django.conf.urls import patterns
from django.conf.urls import url

from .views import DashboardView
from .views import dashboard_view_factory


urlpatterns = patterns(
    '',
    url(
        r'^(?P<dashboard>[\w-]+)/$',
        DashboardView.as_view(),
        name="dashboard",
    ),
    url(
        r'^(?P<dashboard>[\w-]+)/(?P<category>[\w-]+)/(?P<view>[\w-]+)/$',
        dashboard_view_factory,
        name="dashboard_view",
    ),
)
