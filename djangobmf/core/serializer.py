#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals


class Serializer(object):
    def __init__(self, model, iterable, **kwargs):
        self.model = model
        self.data = iterable

    def serialize(self):
        return self._serialize()

    def _serialize(self):
        l = []
        for d in self.data:
            l.append({
                'pk': d.pk,
                'name': str(d),
                'url': d.bmfmodule_detail()
            })
        return l
