#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.permissions import ModulePermission


class TimesheetPermission(ModulePermission):

    def filter_queryset(self, qs, user, model_cls):
        if user.has_perm('%s.can_manage' % model_cls._meta.app_label, model_cls):
            return qs
        return qs.filter(employee=user.djangobmf.employee or -1)
