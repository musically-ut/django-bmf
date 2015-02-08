#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.timezone import now

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView

from .forms import InvoiceUpdateForm
from .forms import InvoiceCreateForm


class InvoiceCreateView(ModuleCreateView):
    form_class = InvoiceCreateForm

    def get_initial(self):
        self.initial.update({
            'date': now(),
            'employee': getattr(self.request.user, 'djangobmf_employee', None),
        })
        return super(InvoiceCreateView, self).get_initial()


class InvoiceUpdateView(ModuleUpdateView):
    form_class = InvoiceUpdateForm
