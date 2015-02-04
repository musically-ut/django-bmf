#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import ViewFactory
from djangobmf.categories import ProjectManagement
from djangobmf.sites import site
from djangobmf.models import Serializer

from .models import Task
from .models import Goal

from .views import TaskGetView

from .views import GoalCloneView
from .views import GoalDetailView
from .views import GoalGetView

class TaskSerializer(Serializer):
    def serialize(self):
        l = []
        for d in self.data:
            l.append({
                # TODO validate summary with regex (at model level)
                'summary': d.summary if d.summary.strip() else '---',
                'completed': d.completed,
                'employee': str(d.employee) if d.employee else None,
                'state': str(d.state),
                'state_name': str(d._bmfworkflow._current_state),
                # TODO: not the ideal solution ... better: use angular to format the date at the client
                'modified': date_format(d.modified, "SHORT_DATE_FORMAT"),
                'goal': str(d.goal) if d.goal else None,
                'project': str(d.project) if d.project else None,
                'url': d.bmfmodule_detail(),
            })
        return l


site.register_module(Task, **{
    'get': TaskGetView,
    'serializer': TaskSerializer,
})


site.register_module(Goal, **{
    'get': GoalGetView,
    'clone': GoalCloneView,
    'detail': GoalDetailView,
})


class GoalCategory(BaseCategory):
    name = _('Goals')
    slug = "goals"


class TaskCategory(BaseCategory):
    name = _('Tasks')
    slug = "tasks"


site.register_dashboards(
    ProjectManagement(
        GoalCategory(
            ViewFactory(
                model=Goal,
                name=_("My goals"),
                slug="my",
                manager="mygoals",
            ),
            ViewFactory(
                model=Goal,
                name=_("Active goals"),
                slug="active",
                manager="active",
            ),
            ViewFactory(
                model=Goal,
                name=_("Archive"),
                slug="archive",
            ),
        ),
        TaskCategory(
            ViewFactory(
                model=Task,
                name=_("My tasks"),
                slug="my",
                manager="mytasks",
            ),
            ViewFactory(
                model=Task,
                name=_("Todolist"),
                slug="todo",
                manager="todo",
            ),
            ViewFactory(
                model=Task,
                name=_("Availalbe tasks"),
                slug="available",
                manager="available",
            ),
            ViewFactory(
                model=Task,
                name=_("Open tasks"),
                slug="open",
                manager="active",
            ),
            ViewFactory(
                model=Task,
                name=_("Archive"),
                slug="archive",
            ),
        ),
    ),
)
