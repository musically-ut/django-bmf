#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.formats import date_format

from djangobmf.serializers import ModuleSerializer

from rest_framework import serializers

from .models import Goal
from .models import Task


class GoalSerializer(ModuleSerializer):
    project_name = serializers.ReadOnlyField(source='project.name')
    referee_name = serializers.ReadOnlyField(source='referee.name')
    state_summary = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = (
            'completed',
            'summary',
            'referee',
            'referee_name',
            'project',
            'project_name',
            'state',
            'state_summary',
            'bmfdetail',
        )

    def get_state_summary(self, obj):
        return obj.get_states()


class TaskSerializer(ModuleSerializer):
    state_key = serializers.ReadOnlyField(source='state.key')
    project_name = serializers.ReadOnlyField(source='project.name')
    employee_name = serializers.ReadOnlyField(source='employee.name')
    goal_summary = serializers.ReadOnlyField(source='goal.summary')
    modified_date = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'state',
            'state_key',
            'summary',
            'completed',
            'project',
            'project_name',
            'goal',
            'goal_summary',
            'employee',
            'employee_name',
            'modified',
            'modified_date',
            'bmfdetail',
        )

    def get_modified_date(self, obj):
        return date_format(obj.modified, "SHORT_DATE_FORMAT")
