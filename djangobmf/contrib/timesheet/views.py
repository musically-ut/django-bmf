#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView

from .forms import TimesheetCreateForm
from .forms import TimesheetUpdateForm


class CreateView(ModuleCreateView):
    form_class = TimesheetCreateForm

    def get_initial(self):
        self.initial.update({
            'employee': getattr(self.request.user, 'djangobmf_employee', None),
        })
        return super(CreateView, self).get_initial()


class UpdateView(ModuleUpdateView):
    form_class = TimesheetUpdateForm
