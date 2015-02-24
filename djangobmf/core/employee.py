#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps

from djangobmf.conf import settings


class Employee(object):

    def __init__(self, user):

        try:
            self.employee_cls = apps.get_model(settings.CONTRIB_EMPLOYEE)
            self.has_employee = True
        except LookupError:
            self.employee_cls = None
            self.has_employee = False

        try:
            self.team_cls = apps.get_model(settings.CONTRIB_TEAM)
            self.has_team = True
        except LookupError:
            self.team_cls = None
            self.has_team = False

        self.user = user
        self._employee = None
        self._evalteam = False
        self._team = []

    @property
    def employee(self):
        if not self.has_employee or self._employee:
            return self._employee
        self._employee = self.employee_cls.objects.get(user=self.user)
        return self._employee

    @property
    def team(self):
        if not self.has_employee or not self.has_team or not self.employee or self._evalteam:
            return self._team
        self._team = self.team_cls.objects.filter(members=self.employee).values_list("id", flat=True)
        self._evalteam = True
        return self._team

    def has_perms(self, perms, module, obj=None):
        return True
