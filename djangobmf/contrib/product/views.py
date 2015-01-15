#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetailView
from djangobmf.views import ModuleListView

from .forms import ProductUpdateForm
from .forms import ProductCreateForm


class ProductIndexView(ModuleListView):
    name = _("All Products")
    slug = "all"


class ProductCreateView(ModuleCreateView):
    form_class = ProductCreateForm


class ProductUpdateView(ModuleUpdateView):
    form_class = ProductUpdateForm


class ProductDetailView(ModuleDetailView):
    pass
