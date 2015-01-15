#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# from django.utils.text import slugify

from djangobmf.views import ModuleListView

# import logging
# logger = logging.getLogger(__name__)


class Workspace(object):
    """
    Object internally used to register modules
    """

    def __init__(self, model, name=None, slug=None, view=None, **kwargs):
        self.model = model
        self.name = name
        self.slug = slug
        self.view = view or ModuleListView
        self.kwargs = kwargs
