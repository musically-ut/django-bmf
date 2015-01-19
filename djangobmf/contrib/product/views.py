#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView

from .forms import ProductUpdateForm
from .forms import ProductCreateForm


class ProductCreateView(ModuleCreateView):
    form_class = ProductCreateForm


class ProductUpdateView(ModuleUpdateView):
    form_class = ProductUpdateForm
