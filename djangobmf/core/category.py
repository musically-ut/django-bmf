#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from .view import View


# TODO add validation for name and slug
class Category(object):
    # Names are passed through to the views they are also translated
    name = None

    # The slug is the unique identifier of the category. Categories with
    # the same slug are merged
    slug = None

    def __init__(self, *args):
        self.data = []
        for view in args:
            self.add_view(view)

        # we add a key to add a unique identifier
        # the key is equal to the slug (for now) but this
        # gives us the opportunity to add i18n urls later
        self.key = self.slug

    def __bool__(self):
        return bool(self.data)

    def __nonzero__(self):
        return self.__bool__()

    def __len__(self):
        return len(self.data)

    def __eq__(self, other):
        if isinstance(other, Category):
            return self.key == other.key
        else:
            return False

    def __iter__(self):
        return self.data.__iter__()

    def __getitem__(self, key):
        data = [i for i in self.data if i.key == key]
        if len(data) == 1:
            return data[0]
        raise KeyError(key)

    def __contains__(self, item):
        if isinstance(item, View):
            key = item.key
        else:
            key = item
        return key in [i.key for i in self.data]

    def add_view(self, view):
        """
        Adds a view to the category
        """
        if view not in self.data:
            self.data.append(view)

    def merge(self, other):
        """
        merges two categories
        """
        for view in other.data:
            self.add_view(view)
