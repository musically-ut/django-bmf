#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import TestCase

from djangobmf.views import ModuleGenericBaseView
from djangobmf.views import ModuleListView
from djangobmf.views import ModuleFilterView
from djangobmf.views import ModuleTreeView
from djangobmf.views import ModuleCategoryView
from djangobmf.views import ModuleArchiveView
from djangobmf.views import ModuleLetterView
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

    @expectedFailure
    def test_viewmixins(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED
