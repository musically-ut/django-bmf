#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

"""
This is a normal urlconf. it is imported from djangobmf.sites.site.get_url, where
the module views get appended by an '^module/' expression
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.http import last_modified

from djangobmf import get_version
from djangobmf.views import ModuleOverviewView
from djangobmf.views.configuration import ConfigurationView
from djangobmf.views.configuration import ConfigurationEdit
from djangobmf.views.dashboard import DashboardView
from djangobmf.views.dashboard import dashboard_view_factory
from djangobmf.views.document import DocumentCreateView
from djangobmf.views.document import DocumentListView
from djangobmf.views.document import DocumentDownloadView


@cache_page(86400, key_prefix='bmf-js18n-%s' % get_version())
@last_modified(lambda req, **kw: timezone.now())
def i18n_javascript(request):
    """
    Displays the i18n JavaScript that the Django admin requires.
    """
    if settings.USE_I18N:  # pragma: no cover
        from django.views.i18n import javascript_catalog
    else:  # pragma: no cover
        from django.views.i18n import null_javascript_catalog as javascript_catalog
    return javascript_catalog(request, packages=['djangobmf'])


urlpatterns = patterns(
    '',
    url(r'^$', DashboardView.as_view(), name="dashboard"),
    url(r'^accounts/', include('djangobmf.account.urls')),

    #   r'^api/module/' via sites

    # --- Configuration
    url(
        r'^config/$', ConfigurationView.as_view(), name="configuration",
    ),
    url(
        r'^config/(?P<app_label>[\w_]+)/(?P<name>[\w_]+)/$',
        ConfigurationEdit.as_view(), name="configuration",
    ),

    #   r'^detail/' via sites

    # --- Dashboard
    url(
        r'^dashboard/(?P<dashboard>[\w-]+)/$',
        DashboardView.as_view(),
        name="dashboard",
    ),
    url(
        r'^dashboard/(?P<dashboard>[\w-]+)/(?P<category>[\w-]+)/(?P<view>[\w-]+)/$',
        dashboard_view_factory,
        name="dashboard_view",
    ),

    # --- Document
    url(
        r'^documents/$',
        DocumentListView.as_view(),
        name="documents",
    ),
    url(
        r'^documents/static/$',
        DocumentListView.as_view(),
        name="documents",
        kwargs={'static': True},
    ),
    url(
        r'^documents/customer/(?P<pk>[0-9]+)/$',
        DocumentListView.as_view(),
        name="documents",
        kwargs={'customer': True},
    ),
    url(
        r'^documents/customer/(?P<pk>[0-9]+)/(?P<ct>[0-9]+)/$',
        DocumentListView.as_view(),
        name="documents",
        kwargs={'customer': True},
    ),
    url(
        r'^documents/project/(?P<pk>[0-9]+)/$',
        DocumentListView.as_view(),
        name="documents",
        kwargs={'project': True},
    ),
    url(
        r'^documents/project/(?P<pk>[0-9]+)/(?P<ct>[0-9]+)/$',
        DocumentListView.as_view(),
        name="documents",
        kwargs={'project': True},
    ),
    url(
        r'^documents/add/(?P<ct>[0-9]+)/(?P<pk>[0-9]+)/$',
        DocumentCreateView.as_view(),
        name="document-add",
    ),
    url(
        r'^documents/get/(?P<pk>[0-9]+)/$',
        DocumentDownloadView.as_view(),
        name="document-get",
    ),

    url(r'^i18n/', i18n_javascript, name="jsi18n"),
    #  url(r'^messages/', include('djangobmf.message.urls')),
    url(r'^modules/$', ModuleOverviewView.as_view(), name="modules"),
    url(r'^notifications/', include('djangobmf.notification.urls')),
    url(r'^wizard/', include('djangobmf.wizard.urls')),
)
