#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site
from djangobmf.categories import BaseCategory
from djangobmf.categories import ViewFactory
from djangobmf.categories import Sales

from .apps import ProductConfig

from .models import Product
from .models import PRODUCT_SERVICE

from .views import ProductCreateView
from .views import ProductUpdateView


site.register_module(Product, **{
    'create': ProductCreateView,
    'update': ProductUpdateView,
})


site.register_settings(ProductConfig.label, {
    'default': forms.ModelChoiceField(queryset=Product.objects.filter(type=PRODUCT_SERVICE)),
})


class ProductCategory(BaseCategory):
    name = _('Products')
    slug = "products"


site.register_dashboards(
    Sales(
        ProductCategory(
            ViewFactory(
                model=Product,
                name=_("Sellable products"),
                slug="sell",
                manager="can_sold",
            ),
            ViewFactory(
                model=Product,
                name=_("Purchaseable products"),
                slug="purchase",
                manager="can_purchased",
            ),
            ViewFactory(
                model=Product,
                name=_("All products"),
                slug="all",
            ),
        ),
    ),
)
