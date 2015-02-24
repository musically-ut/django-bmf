#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.serializers import ModuleSerializer

from .models import Goal
from .models import Task


class GoalSerializer(ModuleSerializer):
    class Meta:
        model = Goal


class TaskSerializer(ModuleSerializer):
    class Meta:
        model = Task
