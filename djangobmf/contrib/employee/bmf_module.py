#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import ViewFactory
from djangobmf.categories import HumanResources
from djangobmf.sites import site

from .models import Employee


site.register_module(Employee, **{
})


class EmployeeCategory(BaseCategory):
    name = _('Employees')
    slug = "employees"


site.register_dashboards(
    HumanResources(
        EmployeeCategory(
            ViewFactory(
                model=Employee,
                name=_("All Employees"),
                slug="all",
            ),
        ),
    ),
)
