#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site
from djangobmf.categories import BaseCategory
from djangobmf.categories import Accounting

from .models import Tax
from .views import TaxIndexView


site.register_module(Tax)


class TaxCategory(BaseCategory):
    name = _('Taxes')
    slug = "taxes"


site.register_dashboard(Accounting)
site.register_category(Accounting, TaxCategory)
site.register_view(Tax, TaxCategory, TaxIndexView)
