#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import TestCase

from djangobmf.views import ModuleListView
from djangobmf.views import ModuleActivityMixin
from djangobmf.views import ModuleFilesMixin
from djangobmf.views import ModuleFormMixin
from djangobmf.views import ModuleDetailView
from djangobmf.views import ModuleAutoDetailView
from djangobmf.views import ModuleReportView
from djangobmf.views import ModuleCloneView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleDeleteView
from djangobmf.views import ModuleWorkflowView
from djangobmf.views import ModuleFormAPI
from djangobmf.views import ModuleOverviewView

from unittest import expectedFailure

from .models import TestView

class ViewsTests(TestCase):

    def test_views_ModuleListView_get_template_names_default(self):
        obj = ModuleListView()
        obj.model = TestView
        self.assertEqual(obj.get_template_names(), ['appapis/testview_bmfgeneric.html', 'djangobmf/module_generic.html'])

    def test_views_ModuleListView_get_template_names_fixed(self):
        obj = ModuleListView()
        obj.model = TestView
        obj.template_name = 'test.html'
        self.assertEqual(obj.get_template_names(), ['test.html'])

    @expectedFailure
    def test_views_ModuleListView(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleActivityMixin(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleFilesMixin(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleFormMixin(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleDetailView(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleAutoDetailView(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleReportView(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleCloneView(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleUpdateView(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleCreateView(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleDeleteView(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleWorkflowView(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleFormAPI(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_views_ModuleOverviewView(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED
