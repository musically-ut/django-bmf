#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps

from djangobmf.conf import settings


class Employee(object):

    try:
        employee_cls = apps.get_model(settings.CONTRIB_EMPLOYEE)
        has_employee = True
    except LookupError:
        employee_cls = None
        has_employee = False

    try:
        team_cls = apps.get_model(settings.CONTRIB_TEAM)
        has_team = True
    except LookupError:
        team_cls = None
        has_team = False

    def __init__(self, user):
        self.user = user
        self._employee = None
        self._evalteam = False
        self._team = []

    @property
    def employee(self):
        if not self.has_employee or self._employee:
            return self._employee
        self._employee = employee_cls.objects.get(user=self.user)
        return self._employee

    @property
    def team(self):
        if not self.has_team or not self.employee or self._evalteam:
            return self._team
        self._team = team_cls.objects.filter(members=self.employee).values_list("id", flat=True)
        self._evalteam = True
        return self._team

    def has_perms(self, perms, module, obj=None):
        return True
