#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleCloneView
from djangobmf.views import ModuleDetailView
from djangobmf.views import ModuleGetView
from djangobmf.views import ModuleListView

from .forms import GoalCloneForm


class GoalGetView(ModuleGetView):
    def get_item_data(self, data):
        l = []
        for d in data:
            l.append({
                'name': str(d),
                'completed': d.completed,
                'referee': str(d.referee),
                'project': str(d.project),
                'url': d.bmfmodule_detail(),
                'states': d.get_states(),
            })
        return l


class TaskGetView(ModuleGetView):
    def get_item_data(self, data):
        l = []
        for d in data:
            l.append({
                'summary': d.summary,
                'completed': d.completed,
                'employee': str(d.employee),
                'state': str(d.state),
                'modified': d.modified,
                'goal': str(d.goal),
                'project': str(d.project),
                'url': d.bmfmodule_detail(),
            })
        return l


class ArchiveGoalView(ModuleListView):
    slug = "archive"
    name = _("Archive")


class ActiveGoalView(ModuleListView):
    slug = "active"
    name = _("Active Goals")
    manager = "active"

    # TODO: REMOVE ME
    def get_queryset(self):  # noqa
        return super(ActiveGoalView, self).get_queryset().filter(completed=False)


class MyGoalView(ModuleListView):
    slug = "my"
    name = _("My Goals")
    manager = "mygoals"

    # TODO: REMOVE ME
    def get_queryset(self):  # noqa
        return super(MyGoalView, self).get_queryset() \
            .filter(completed=False, referee=getattr(self.request.user, 'djangobmf_employee', -1))


class ArchiveTaskView(ModuleListView):
    slug = "archive"
    name = _("Archive")
    date_resolution = "month"


class OpenTaskView(ModuleListView):
    slug = "open"
    name = _("Open Tasks")
    manager = "active"

    def get_queryset(self):  # noqa
        return super(OpenTaskView, self).get_queryset().filter(completed=False)


class AvailableTaskView(ModuleListView):
    slug = "available"
    name = _("Available Tasks")
    manager = "availalbe"

    def get_queryset(self):  # noqa
        return super(AvailableTaskView, self).get_queryset().filter(employee=None, completed=False)


class MyTaskView(ModuleListView):
    slug = "my"
    name = _("My Tasks")
    manager = "mytasks"

    def get_queryset(self):  # noqa
        return super(MyTaskView, self).get_queryset() \
            .filter(completed=False, employee=getattr(self.request.user, 'djangobmf_employee', -1))


class TodoTaskView(ModuleListView):
    slug = "todo"
    name = _("Todolist")
    manager = "todo"

    def get_queryset(self):  # noqa
        return super(TodoTaskView, self).get_queryset() \
            .filter(completed=False, state__in=["todo", "started", "review"],
                    employee=getattr(self.request.user, 'djangobmf_employee', -1))


class GoalCloneView(ModuleCloneView):
    form_class = GoalCloneForm

    def clone_object(self, formdata, instance):
        instance.completed = False

    def clone_related_objects(self, formdata, old_object, new_object):
        if formdata['copy_tasks']:
            for task in old_object.task_set.all():
                task.pk = None
                task.goal = new_object
                task.project = new_object.project
                if formdata['clear_employee']:
                    task.employee = None
                task.due_date = None
                task.completed = False
                task.work_date = None
                task.seconds_on = 0
                setattr(task, task._bmfmeta.workflow_field, task._bmfmeta.workflow._default_state_key)
                task.save()


class GoalDetailView(ModuleDetailView):
    def get_context_data(self, **kwargs):
        tasks = {
            'open': [],
            'hold': [],
            'done': [],
        }
        for task in self.object.task_set.all():
            if task.state in ["open", "started", "new"]:
                tasks["open"].append(task)
            elif task.state in ["hold", "review", "todo"]:
                tasks["hold"].append(task)
            else:
                tasks["done"].append(task)

        kwargs.update({
            'tasks': tasks,
        })
        return super(GoalDetailView, self).get_context_data(**kwargs)
