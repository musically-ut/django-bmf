#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import Sales
from djangobmf.sites import site

from .models import Address

from .views import AddressIndexView


site.register_module(Address)


class AddressCategory(BaseCategory):
    name = _('Address')
    slug = "address"


site.register_dashboard(Sales)

site.register_category(Sales, AddressCategory)
site.register_view(Address, AddressCategory, AddressIndexView)
