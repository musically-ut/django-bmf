#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.core.dashboard import Dashboard as BaseDashboard
from djangobmf.core.category import Category as BaseCategory
from djangobmf.core.view import View as ViewFactory

from djangobmf.sites import Dashboard


__all__ = [
    'ViewFactory',
    'Dashboard',
    'BaseDashboard',
    'BaseCategory',
    'ProjectManagement',
    'DocumentManagement',
    'Sales',
    'CustomerRelationship',
    'Accounting',
    'Warehouse',
    'TimeAndAttendance',
]


# --- Predefined Dashboards ---------------------------------------------------


class ProjectManagement(Dashboard):
    name = _('Project Management')
    slug = "projects"


class DocumentManagement(Dashboard):
    name = _('Document Management')
    slug = "dms"


class Sales(Dashboard):
    name = _('Sales')
    slug = "sales"


class HumanResources(Dashboard):
    name = _('Human Resources')
    slug = "hr"


class CustomerRelationship(Dashboard):
    name = _('Customer Relationship')
    slug = "cr"


class Accounting(Dashboard):
    name = _('Accounting')
    slug = "accounting"


class Warehouse(Dashboard):
    name = _('Warehouse')
    slug = "warehouse"


class TimeAndAttendance(Dashboard):
    name = _('Time and attendance')
    slug = "attendance"
