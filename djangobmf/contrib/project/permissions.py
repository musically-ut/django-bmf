#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db.models import Q

from djangobmf.permissions import ModulePermission


class ProjectPermission(ModulePermission):

    def filter_queryset(self, qs, user, model_cls):
        if user.has_perm('%s.can_manage' % model_cls._meta.app_label, model_cls):
            return qs
        return qs.filter(
            Q(employees=getattr(user, 'djangobmf_employee', -1)) |
            Q(team__in=getattr(user, 'djangobmf_teams', []))
        )
