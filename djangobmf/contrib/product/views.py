#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleDetailView
from djangobmf.views import ModuleUpdateView

from .forms import ProductUpdateForm
from .forms import ProductCreateForm


class ProductCreateView(ModuleCreateView):
    form_class = ProductCreateForm


class ProductUpdateView(ModuleUpdateView):
    form_class = ProductUpdateForm


class ProductDetailView(ModuleDetailView):

    def get_context_data(self, **kwargs):
        unit_exact, net, gross, used_taxes = self.object.calc_tax(
            1.0, self.object.price, related=True
        )

        return super(ProductDetailView, self).get_context_data(
            calc_net=net,
            calc_gross=gross,
            taxes=used_taxes,
        )
