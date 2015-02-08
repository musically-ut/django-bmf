#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.core.dashboard import Dashboard as BaseDashboard
from djangobmf.core.category import Category as BaseCategory
from djangobmf.core.view import View as ViewFactory


__all__ = [
    'ViewFactory',
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


class ProjectManagement(BaseDashboard):
    name = _('Project Management')
    slug = "projects"


class DocumentManagement(BaseDashboard):
    name = _('Document Management')
    slug = "dms"


class Sales(BaseDashboard):
    name = _('Sales')
    slug = "sales"


class HumanResources(BaseDashboard):
    name = _('Human Resources')
    slug = "hr"


class CustomerRelationship(BaseDashboard):
    name = _('Customer Relationship')
    slug = "cr"


class Accounting(BaseDashboard):
    name = _('Accounting')
    slug = "accounting"


class Warehouse(BaseDashboard):
    name = _('Warehouse')
    slug = "warehouse"


class TimeAndAttendance(BaseDashboard):
    name = _('Time and attendance')
    slug = "attendance"
