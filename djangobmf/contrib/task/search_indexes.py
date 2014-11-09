#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from .models import Goal
from .models import Task

from djangobmf.search_indexes import ContribIndex

from haystack import indexes


class GoalIndex(ContribIndex, indexes.Indexable):
    def get_model(self):
        return Goal


class TaskIndex(ContribIndex, indexes.Indexable):
    def get_model(self):
        return Task
