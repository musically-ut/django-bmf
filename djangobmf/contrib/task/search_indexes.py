#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from .models import Goal
from .models import Task

from djangobmf.search_fields import CommentField

from haystack import indexes

class GoalIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    comments = CommentField()
    modified = indexes.DateTimeField(model_attr='modified')

    def get_model(self):
        return Goal

class TaskIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    comments = CommentField()
    modified = indexes.DateTimeField(model_attr='modified')

    def get_model(self):
        return Task

#   def index_queryset(self, using=None):
#       print(using)
#       """Used when the entire index for model is updated."""
#       return self.get_model().objects.filter(action=ACTION_COMMENT)
