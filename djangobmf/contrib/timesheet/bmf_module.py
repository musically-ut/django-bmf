#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _

from djangobmf.sites import site
from djangobmf.categories import BaseCategory
from djangobmf.categories import ViewFactory
from djangobmf.categories import TimeAndAttendance
from djangobmf.models import Serializer

from .models import Timesheet

from .views import CreateView
from .views import UpdateView


class TimesheetSerializer(Serializer):
    def serialize(self):
        l = []
        for obj in self.data:
            l.append({
                'date': date_format(obj.start, "SHORT_DATE_FORMAT"),
                'summary': obj.summary,
                'start': obj.start,
                'end': obj.end,
                'employee': str(obj.employee) if obj.employee else None,
                'project': str(obj.project) if obj.project else None,
                'task': str(obj.task) if obj.task else None,
                'url': obj.bmfmodule_detail(),
            })
        return l


site.register_module(Timesheet, **{
    'create': CreateView,
    'update': UpdateView,
    'serializer': TimesheetSerializer,
})


class TimesheetCategory(BaseCategory):
    name = _('Timesheets')
    slug = "timesheets"


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
