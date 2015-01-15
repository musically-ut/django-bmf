#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from collections import OrderedDict


class Category(object):
    name = None
    slug = None

    def __init__(self, **kwargs):
        # TODO add validation
        # if not self.name or not name self.slug:
        #     raise

        self.data = OrderedDict()
        self.key = self.slug

        for key, item in kwargs.items():
            self.data[key] = item

    def merge(self, other):
        pass
