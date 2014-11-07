#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from haystack.indexes import EdgeNgramField


class CommentField(EdgeNgramField):
    def __init__(self, *args, **kwargs):
        defaults = {
            'document': False,
            'indexed': True,
            'use_template': False,
            'boost': 0.7,
        }
        defaults.update(kwargs)
        super(CommentField, self).__init__(*args, **defaults)

    def prepare(self, obj):
        data = []
        for comment in obj.djangobmf_activity.comments():
            data.append(comment.topic)
            data.append(comment.text)
        return '\n'.join(data)
