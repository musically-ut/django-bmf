#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db.models import Q

from djangobmf.permissions import ModulePermission


class GoalPermission(ModulePermission):

    def filter_queryset(self, qs, user, model_cls):
        if user.has_perm('%s.can_manage' % model_cls._meta.app_label, model_cls):
            return qs

        qs_filter = Q(referee=user.djangobmf.employee or -1)
        qs_filter |= Q(employees=user.djangobmf.employee or -1)
        qs_filter |= Q(team__in=user.djangobmf.team)

        if hasattr(model_cls, "project"):  # pragma: no branch
            project = model_cls._meta.get_field_by_name("project")[0].model
            if user.has_perm('%s.can_manage' % project._meta.app_label, project):
                qs_filter |= Q(project__isnull=False)
            else:
                qs_filter |= Q(project__isnull=False, project__employees=user.djangobmf.employee or -1)
                qs_filter |= Q(project__isnull=False, project__team__in=user.djangobmf.team)
        return qs.filter(qs_filter)


class TaskPermission(ModulePermission):

    def filter_queryset(self, qs, user, model_cls):
        qs_filter = Q(project__isnull=True, goal__isnull=True)
        qs_filter |= Q(employee=user.djangobmf.employee or -1)
        qs_filter |= Q(in_charge=user.djangobmf.employee)

        if hasattr(model_cls, "goal"):  # pragma: no branch
            goal = model_cls._meta.get_field_by_name("goal")[0].model
            if user.has_perm('%s.can_manage' % goal._meta.app_label, goal):
                qs_filter |= Q(goal__isnull=False)
            else:
                qs_filter |= Q(goal__isnull=False, goal__referee=user.djangobmf.employee or -1)
                qs_filter |= Q(goal__isnull=False, goal__employees=user.djangobmf.employee or -1)
                qs_filter |= Q(goal__isnull=False, goal__team__in=user.djangobmf.team)

        if hasattr(model_cls, "project"):  # pragma: no branch
            project = model_cls._meta.get_field_by_name("project")[0].model
            if user.has_perm('%s.can_manage' % project._meta.app_label, project):
                qs_filter |= Q(project__isnull=False)
            else:
                qs_filter |= Q(project__isnull=False, project__employees=user.djangobmf.employee or -1)
                qs_filter |= Q(project__isnull=False, project__team__in=user.djangobmf.team)

        return qs.filter(qs_filter)
