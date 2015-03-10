#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.models import Configuration
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView

from .forms import CompanyForm
from .forms import CustomerForm


class BaseCreateView(ModuleCreateView):
    def get_initial(self):
        self.initial.update({
            'asset_account': Configuration.get_setting('bmfcontrib_accounting', 'customer'),
            'liability_account': Configuration.get_setting('bmfcontrib_accounting', 'supplier'),
        })
        return super(BaseCreateView, self).get_initial()


class CompanyCreateView(BaseCreateView):
    form_class = CompanyForm

    def form_valid(self, form):
        form.instance.is_company = True
        return super(CompanyCreateView, self).form_valid(form)


class CustomerCreateView(BaseCreateView):
    form_class = CustomerForm

    def form_valid(self, form):
        form.instance.is_company = False
        return super(CustomerCreateView, self).form_valid(form)


class UpdateView(ModuleUpdateView):
    def get_form_class(self, *args, **kwargs):
        if self.object.is_company:
            return CompanyForm
        return CustomerForm
