#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site

from .apps import ProductConfig
from djangobmf.categories import BaseCategory
from djangobmf.categories import Sales


from .models import Product
from .models import PRODUCT_SERVICE
from .views import ProductIndexView
from .views import ProductCreateView
from .views import ProductDetailView
from .views import ProductUpdateView

site.register_module(Product, **{
    'create': ProductCreateView,
    'detail': ProductDetailView,
    'update': ProductUpdateView,
})

SETTINGS = {
    'default': forms.ModelChoiceField(queryset=Product.objects.filter(type=PRODUCT_SERVICE)),
}
site.register_settings(ProductConfig.label, SETTINGS)


class ProductCategory(BaseCategory):
    name = _('Products')
    slug = "products"


site.register_dashboard(Sales)
site.register_category(Sales, ProductCategory)
site.register_view(Product, ProductCategory, ProductIndexView)
