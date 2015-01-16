#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView

from .forms import InvoiceUpdateForm
from .forms import InvoiceCreateForm


class InvoiceCreateView(ModuleCreateView):
    form_class = InvoiceCreateForm


class InvoiceUpdateView(ModuleUpdateView):
    form_class = InvoiceUpdateForm
