#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import ViewFactory
from djangobmf.categories import Accounting
from djangobmf.sites import site

from .models import Tax


site.register_module(Tax)


class TaxCategory(BaseCategory):
    name = _('Taxes')
    slug = "taxes"


site.register_dashboards(
    Accounting(
        TaxCategory(
            ViewFactory(
                model=Tax,
                name=_("All Taxes"),
                slug="all",
            ),
        ),
    ),
)
