#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.utils import six
from django.utils.text import slugify

from djangobmf.core.serializer import Serializer
from djangobmf.views import ModuleCloneView
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleDeleteView
from djangobmf.views import ModuleDetailView
from djangobmf.views import ModuleFormAPI
from djangobmf.views import ModuleGetView
from djangobmf.views import ModuleListView
from djangobmf.views import ModuleReportView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleWorkflowView

import logging
logger = logging.getLogger(__name__)


class Module(object):
    """
    Object internally used to register modules
    """

    def __init__(self, model, **options):
        self.model = model
        self.dashboards = []
        self.create = options.get('create', ModuleCreateView)
        self.detail = options.get('detail', ModuleDetailView)
        self.update = options.get('update', ModuleUpdateView)
        self.delete = options.get('delete', ModuleDeleteView)
        self.clone = options.get('clone', ModuleCloneView)
        self.get = options.get('get', ModuleGetView)
        self.serializer = options.get('serializer', Serializer)
        self.report = options.get('report', None)
        self.detail_urlpatterns = options.get('detail_urlpatterns', None)
        self.api_urlpatterns = options.get('api_urlpatterns', None)
        self.manager = {}

    def list_reports(self):
        if hasattr(self, 'listed_reports'):
            return self.listed_reports
        self.listed_reports = []

        if isinstance(self.report, dict):
            for label, view in six.iteritems(self.report):
                key = slugify(label)
                if isinstance(view, (list, tuple)) and len(view) == 2:
                    # overwrite the label, and correct the view
                    label = slugify(view[0])
                    view = view[1]
            self.listed_reports.append((key, label, view))

        elif isinstance(self.report, bool):
            self.listed_reports.append(('default', 'default', ModuleReportView))
        elif self.report and issubclass(self.report, ModuleReportView):
            self.listed_reports.append(('default', 'default', self.report))

        return self.listed_reports

    def list_creates(self):
        if hasattr(self, 'listed_creates'):
            return self.listed_creates
        self.listed_creates = []

        if isinstance(self.create, dict):
            for label, view in six.iteritems(self.create):
                key = slugify(label)

                if isinstance(view, (list, tuple)) and len(view) == 2:
                    # overwrite the label, and use the correct the view function
                    label = view[0]
                    view = view[1]
                self.listed_creates.append((key, label, view))

        elif issubclass(self.create, ModuleCreateView):
            self.listed_creates.append(('default', 'default', self.create))

        # update model with all create views
        self.model._bmfmeta.create_views = self.listed_creates

        return self.listed_creates

    def get_detail_urls(self):
        reports = self.list_reports()

        urlpatterns = patterns(
            '',
            url(
                r'^$',
                self.detail.as_view(model=self.model, reports=reports),
                name='detail',
            ),
        )

        # add custom url patterns
        if self.detail_urlpatterns:
            urlpatterns += self.detail_urlpatterns

        return urlpatterns

    def get_api_urls(self):
        reports = self.list_reports()
        creates = self.list_creates()

        urlpatterns = patterns(
            '',
            url(
                r'^$',
                ModuleListView.as_view(model=self.model),
                name='list',
            ),
            url(
                r'^get/$',
                self.get.as_view(
                    model=self.model,
                    serializer=self.serializer,
                ),
                name='get',
            ),
            url(
                r'^get/(?P<manager>\w+)/$',
                self.get.as_view(
                    model=self.model,
                    serializer=self.serializer,
                ),
                name='get',
            ),
            url(
                r'^update/(?P<pk>[0-9]+)/$',
                self.update.as_view(model=self.model),
                name='update',
            ),
            url(
                r'^update/(?P<pk>[0-9]+)/form/$',
                ModuleFormAPI.as_view(
                    model=self.model,
                    form_view=self.update,
                ),
                name='update-form',
            ),
            url(
                r'^delete/(?P<pk>[0-9]+)/$',
                self.delete.as_view(model=self.model),
                name='delete',
            ),
        )
        if self.model._bmfmeta.can_clone:
            urlpatterns += patterns(
                '',
                url(
                    r'^clone/(?P<pk>[0-9]+)/$',
                    self.clone.as_view(model=self.model),
                    name='clone',
                ),
                url(
                    r'^clone/(?P<pk>[0-9]+)/form/$',
                    ModuleFormAPI.as_view(
                        model=self.model,
                        form_view=self.clone,
                    ),
                    name='clone-form',
                ),
            )

        for key, label, view in creates:
            urlpatterns += patterns(
                '',
                url(
                    r'^create/(?P<key>%s)/$' % key,
                    view.as_view(model=self.model),
                    name='create',
                ),
                url(
                    r'^create/(?P<key>%s)/form/$' % key,
                    ModuleFormAPI.as_view(
                        model=self.model,
                        form_view=view,
                    ),
                    name='create-form',
                ),
            )

        for key, label, view in reports:
            urlpatterns += patterns(
                '',
                url(
                    r'^report/(?P<key>%s)/$' % key,
                    view.as_view(model=self.model),
                    name='report',
                ),
            )

        # workflow interactions
        if self.model._bmfmeta.has_workflow:
            urlpatterns += patterns(
                '',
                url(
                    r'^workflow/(?P<pk>[0-9]+)/(?P<transition>\w+)/$',
                    ModuleWorkflowView.as_view(model=self.model),
                    name='workflow',
                ),
            )

        # add custom url patterns
        if self.api_urlpatterns:
            urlpatterns += self.api_urlpatterns

        return urlpatterns
