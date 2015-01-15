#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from .category import Category


class Dashboard(object):
    # Names are passed through to the views they are also translated
    name = None

    # The slug is the unique identifier of the dashboard. Dashboards with
    # the same slug are merged
    slug = None

    def __init__(self, *args):
        self.data = []
        for category in args:
            self.add_category(category)

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
        if isinstance(other, Dashboard):
            return self.key == other.key
        else:
            return False

    def __getitem__(self, key):
        data = [i for i in self.data if i.key == key]
        if len(data) == 1:
            return data[0]
        raise KeyError('key')

    def __contains__(self, item):
        if isinstance(item, Category):
            key = item.key
        else:
            key = item
        return key in [i.key for i in self.data]

    def add_category(self, category):
        """
        Adds a category to the dashboard
        """
        if category in self.data:
            i = self.data.index(category)
            self.data[i].merge(category)
        else:
            self.data.append(category)

    def merge(self, other):
        """
        merges two dashboards
        """
        for category in other.data:
            self.add_category(category)
