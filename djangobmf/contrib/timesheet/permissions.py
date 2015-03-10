#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.permissions import ModulePermission


class TimesheetPermission(ModulePermission):

    def filter_queryset(self, qs, user):
        if user.has_perm('%s.can_manage' % qs.model._meta.app_label, qs.model):
            return qs
        return qs.filter(employee=user.djangobmf.employee or -1)
