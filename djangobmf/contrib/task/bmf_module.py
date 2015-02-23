#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import ViewFactory
from djangobmf.categories import ProjectManagement
from djangobmf.sites import Module
from djangobmf.sites import site
from djangobmf.sites import register

# from djangobmf.contrib.project.categories import ProjectCategory
# from djangobmf.contrib.project.models import Project

from .categories import GoalCategory
from .categories import TaskCategory
from .models import Task
from .models import Goal
from .views import TaskGetView
from .views import GoalCloneView
from .views import GoalDetailView
from .views import GoalGetView


# ass GoalSerializer(Serializer):
#   def serialize(self):
#       l = []
#       for d in self.data:
#           l.append({
#               'name': str(d),
#               'completed': d.completed,
#               'referee': str(d.referee),
#               'project': str(d.project),
#               'url': d.bmfmodule_detail(),
#               'states': d.get_states(),
#           })
#       return l


# ass TaskSerializer(Serializer):
#   def serialize(self):
#       l = []
#       for d in self.data:
#           l.append({
#               # TODO validate summary with regex (at model level)
#               'summary': d.summary if d.summary.strip() else '---',
#               'completed': d.completed,
#               'employee': str(d.employee) if d.employee else None,
#               'state': d.state.key,
#               'state_name': str(d.state),
#               # TODO: not the ideal solution ... better: use angular to format the date at the client
#               'modified': date_format(d.modified, "SHORT_DATE_FORMAT"),
#               'goal': str(d.goal) if d.goal else None,
#               'project': str(d.project) if d.project else None,
#               'url': d.bmfmodule_detail(),
#           })
#       return l


@register(dashboard=ProjectManagement)
class TaskModule(Module):
    model = Task
    get = TaskGetView


@register(dashboard=ProjectManagement)
class GoalModule(Module):
    model = Goal
    get = GoalGetView
    clone = GoalCloneView
    detail = GoalDetailView


@register(dashboard=ProjectManagement)
class GoalCategoryCLS(GoalCategory):
    my = ViewFactory(
        model=Goal,
        slug="my",
        name=_("My goals"),
        manager="mygoals",
    )
    active = ViewFactory(
        model=Goal,
        slug="active",
        name=_("Active goals"),
        manager="active",
    )
    archive = ViewFactory(
        model=Goal,
        slug="archive",
        name=_("Archive"),
    )


@register(dashboard=ProjectManagement)
class TaskCategoryCLS(TaskCategory):
    my = ViewFactory(
        model=Task,
        slug="my",
        name=_("My tasks"),
        manager="mytasks",
    )
    todo = ViewFactory(
        model=Task,
        slug="todo",
        name=_("Todolist"),
        manager="todo",
    )
    available = ViewFactory(
        model=Task,
        slug="available",
        name=_("Availalbe tasks"),
        manager="available",
    )
    open = ViewFactory(
        model=Task,
        slug="open",
        name=_("Open tasks"),
        manager="active",
    )
    archive = ViewFactory(
        model=Task,
        slug="archive",
        name=_("Archive"),
    )


site.register_module(Task, **{
    'get': TaskGetView,
})


site.register_module(Goal, **{
    'get': GoalGetView,
    'clone': GoalCloneView,
    'detail': GoalDetailView,
})


site.register_dashboards(
    ProjectManagement(
        # ProjectCategory(
        #     ViewFactory(
        #         model=Project,
        #         name=_("Open Projects"),
        #         slug="open",
        #         manager='open',
        #         queryset=(Project.objects.filter(goal__pk__gt=0) | Project.objects.filter(task__pk__gt=0)).distinct(),
        #     ),
        # ),
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
