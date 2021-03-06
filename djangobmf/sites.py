#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps

from djangobmf.conf import settings

from djangobmf.core.category import Category
from djangobmf.core.dashboard import Dashboard
from djangobmf.core.module import Module
from djangobmf.core.report import Report
from djangobmf.core.view import View

import logging
logger = logging.getLogger(__name__)


__all__ = [
    'Category',
    'Dashboard',
    'Module',
    'Report',
    'View',
]


# shortcut to the site instance to provide a simple
# syntax to add the framework to external modules
# please note, that this is only available, when the
# apps are loaded (cause the site does some database
# queries). Importing this to early leads to an exception
# which is a feature and not a bug.
if apps.apps_ready:  # pragma: no branch
    site = apps.get_app_config(settings.APP_LABEL).site

    class register(object):  # noqa
        def __init__(self, cls=None, **kwargs):
            self.kwargs = kwargs
            if cls:
                self.register_generic(cls)

        def __call__(self, cls):
            self.register_generic(cls)

        def register_generic(self, cls):
            if "dashboard" in self.kwargs:
                logger.debug('Register Dashboard "%s"' % self.kwargs["dashboard"])
                # if self.kwargs["dashboard"] not in site.dashboards:
                #     # initialize dashboard and append to site
                #     site.dashboards.append(self.kwargs["dashboard"]())

            if issubclass(cls, Category) and 'dashboard' in self.kwargs:
                logger.debug('Register Category "%s"' % cls.__name__)

            if issubclass(cls, Module) and 'dashboard' in self.kwargs:
                logger.debug('Register Module "%s"' % cls.__name__)

    __all__ += [
        'register',
        'site',
    ]
