#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

#from djangobmf.notification.models import Activity
#from djangobmf.notification.models import ACTION_COMMENT

#from haystack import indexes

#class NoteIndex(indexes.SearchIndex, indexes.Indexable):
#    text = indexes.EdgeNgramField(document=True, use_template=True)
#    ct = indexes.CharField(model_attr="parent_ct")
#    modified = indexes.DateTimeField(model_attr='modified')
#
#    def get_model(self):
#        return Activity
#
#    def index_queryset(self, using=None):
#        print(using)
#        """Used when the entire index for model is updated."""
#        return self.get_model().objects.filter(action=ACTION_COMMENT)
