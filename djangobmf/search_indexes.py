#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from djangobmf.notification.models import Activity

from haystack import indexes

# SearchQuerySet().filter(content_type_id__exact=10, content="text").using("default").count()


class ContribIndex(indexes.SearchIndex):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    content_type_id = indexes.IntegerField(faceted=True)
    modified = indexes.DateTimeField(model_attr='modified')

    def prepare_content_type_id(self, obj):
        return ContentType.objects.get_for_model(self.get_model()).pk


class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    content_type_id = indexes.IntegerField(model_attr="parent_ct_id", faceted=True)
    modified = indexes.DateTimeField(model_attr='modified')

    def get_model(self):
        return Activity

    def index_queryset(self, using=None):
        return self.get_model().objects.comments()
