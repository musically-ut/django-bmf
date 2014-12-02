#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleArchiveView
from djangobmf.views import ModuleListView
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetailView

from .forms import QuotationUpdateForm
from .forms import QuotationCreateForm

from .filters import QuotationFilter


class AllQuotationView(ModuleArchiveView):
    name = _("All Quotations")
    slug = "all"
    filterset_class = QuotationFilter


class OpenQuotationView(ModuleListView):
    name = _("Open Quotations")
    slug = "open"
    filterset_class = QuotationFilter

    def get_queryset(self):
        return super(OpenQuotationView, self).get_queryset().filter(completed=False)


class QuotationCreateView(ModuleCreateView):
    form_class = QuotationCreateForm

    def get_initial(self):
        self.initial.update({
            'date': now(),
            'employee': getattr(self.request, 'djangobmf_employee', None),
        })
#       print(self.initial)
        return super(QuotationCreateView, self).get_initial()


class QuotationUpdateView(ModuleUpdateView):
    form_class = QuotationUpdateForm


class QuotationDetailView(ModuleDetailView):
    pass
