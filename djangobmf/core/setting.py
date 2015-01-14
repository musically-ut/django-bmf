#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.apps import apps
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.admin.sites import NotRegistered
from django.contrib.contenttypes.models import ContentType
# from django.core.exceptions import AppRegistryNotReady
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import OperationalError
from django.db.utils import ProgrammingError
from django.utils.module_loading import module_has_submodule
from django.utils.module_loading import import_module
from django.utils import six
from django.utils.text import slugify

from djangobmf.models import Configuration
from djangobmf.views import ModuleCloneView
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleDeleteView
from djangobmf.views import ModuleDetailView
from djangobmf.views import ModuleFormAPI
from djangobmf.views import ModuleGetView
from djangobmf.views import ModuleListView
from djangobmf.views import ModuleReportView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleWorkflowView

from collections import OrderedDict

import copy
import sys

import logging
logger = logging.getLogger(__name__)

SETTING_KEY = "%s.%s"


class Setting(object):
    """
    Object used to register settings
    """
    def __init__(self, app_label, name, field):
        self.app_label = app_label
        self.name = name
        self.field = field

    @property
    def key(self):
        return SETTING_KEY % (self.app_label, self.name)

    @property
    def required(self):
        return self.field.required

    @property
    def changed(self):
        return self.field.initial != self.value

    @property
    def label(self):
        if self.field.label:
            return self.field.label
        return self.key

    @property
    def default(self):
        return self.field.initial

    @property
    def value(self):
        try:
            value = Configuration.objects.get_value(self.app_label, self.name)
        except Configuration.DoesNotExist:
            value = self.field.initial
        return value
