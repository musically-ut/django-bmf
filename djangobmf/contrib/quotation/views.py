#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.timezone import now

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView

from .forms import QuotationUpdateForm
from .forms import QuotationCreateForm


class QuotationCreateView(ModuleCreateView):
    form_class = QuotationCreateForm

    def get_initial(self):
        self.initial.update({
            'date': now(),
            'employee': self.request.user.djangobmf.employee,
        })
        return super(QuotationCreateView, self).get_initial()


class QuotationUpdateView(ModuleUpdateView):
    form_class = QuotationUpdateForm
