#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# from django.conf.urls import patterns

from djangobmf.sites import site

from collections import OrderedDict

from .category import Category


# TODO add validation for name and slug
class Dashboard(object):
    # Names are passed through to the views they are also translated
    name = None

    # The slug is the unique identifier of the dashboard. Dashboards with
    # the same slug are merged
    slug = None

    def __init__(self, *args):
        self.data = OrderedDict()
        self.modules = []
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

    def __iter__(self):
        return self.data.values().__iter__()

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, item):
        if isinstance(item, Category):
            key = item.key
        else:
            key = item
        return key in self.data

    def add_category(self, category):
        """
        Adds a category to the dashboard
        """
        for model in category.models:
            module = site.get_module(model)
            if self not in module.dashboards:
                module.dashboards.append(self)

        if category in self.data.values():
            self.data[category.key].merge(category)
        else:
            self.data[category.key] = category

    def merge(self, other):
        """
        merges two dashboards
        """
        for category in other.data.values():
            self.add_category(category)

#   @property
#   def urls(self):
#       urlpatterns = patterns('')
#       return urlpatterns
