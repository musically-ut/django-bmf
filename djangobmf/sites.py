#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps

from djangobmf.settings import APP_LABEL


# provide the site instance here to provide a simple
# syntax to add the framework to the projects urls.py
if apps.apps_ready:
    site = apps.get_app_config(APP_LABEL).site
    register = site.register
