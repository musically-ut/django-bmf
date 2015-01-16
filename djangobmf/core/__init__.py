#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps

from djangobmf.settings import APP_LABEL


def site_lazy():
    if apps.apps_ready:
        return apps.get_app_config(APP_LABEL).site
    return None
