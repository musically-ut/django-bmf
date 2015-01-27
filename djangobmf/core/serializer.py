#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals


class Serializer(object):
    def __init__(self, *args, **kwargs):
        pass
        
    def serialize(self, obj):
        return self._serialize(obj)
        
    def _serialize(self, obj):
        return {
            'pk': obj.pk,
            'name': str(obj),
            'url': obj.bmfmodule_detail(),
        }
