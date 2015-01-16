#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site
from djangobmf.categories import BaseCategory
from djangobmf.categories import ViewFactory
from djangobmf.categories import TimeAndAttendance

from .models import Timesheet

from .views import CreateView
from .views import UpdateView

site.register_module(Timesheet, **{
    'create': CreateView,
    'update': UpdateView,
})


class TimesheetCategory(BaseCategory):
    name = _('Timesheets')
    slug = "timesheets"


# NEW
site.register_dashboards(
    TimeAndAttendance(
        TimesheetCategory(
            ViewFactory(
                model=Timesheet,
                name=_("My timesheets"),
                slug="mytimesheets",
                manager="mytimesheets",
                date_resolution='week',
            ),
            ViewFactory(
                model=Timesheet,
                name=_("Archive"),
                slug="archive",
                date_resolution='week',
            ),
        ),
    ),
)

# OLD
from .views import ArchiveView
site.register_dashboard(TimeAndAttendance)
site.register_category(TimeAndAttendance, TimesheetCategory)
site.register_view(Timesheet, TimesheetCategory, ArchiveView)
