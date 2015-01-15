#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site
from djangobmf.categories import BaseCategory
from djangobmf.categories import HumanResources

from .models import Employee
from .views import EmployeeIndexView
from .views import EmployeeCreateView

site.register_module(Employee, **{
    'create': EmployeeCreateView,
})


class EmployeeCategory(BaseCategory):
    name = _('Employees')
    slug = "employees"


site.register_dashboard(HumanResources)
site.register_category(HumanResources, EmployeeCategory)
site.register_view(Employee, EmployeeCategory, EmployeeIndexView)
