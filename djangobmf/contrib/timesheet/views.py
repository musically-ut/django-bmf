#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleListView
from djangobmf.views import ModuleUpdateView

from .forms import TimesheetCreateForm
from .forms import TimesheetUpdateForm


class ArchiveView(ModuleListView):
    name = _("Archive")
    slug = "archive"
    date_resolution = 'week'


class CreateView(ModuleCreateView):
    form_class = TimesheetCreateForm


class UpdateView(ModuleUpdateView):
    form_class = TimesheetUpdateForm
