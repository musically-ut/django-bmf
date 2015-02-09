#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.admin.sites import NotRegistered
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured

from djangobmf.core.module import Module
from djangobmf.models import NumberCycle

import logging
logger = logging.getLogger(__name__)


class Site(object):
    """
    Handle modules like the AdminSite from django.contrib.admin.sites
    """

    def __init__(self, namespace=None, app_name=None):
        self.namespace = namespace or "djangobmf"
        self.app_name = app_name or "djangobmf"
        self.clear()

    # TODO add some generic register function, which functions as a decorator and can be used on different objects
    def register(self, *args, **kwargs):  # pragma: no cover
        pass

    def clear(self):
        # true if the site is active, ie loaded
        self.is_active = False

        # combine all registered modules here
        self.modules = {}

        # all currencies should be stored here
        self.currencies = {}

        # all numbercycles are here
        self.numbercycles = []

        # all reports should be stored here
        self.reports = {}

        # all dashboards are stored here
        self.dashboards = []

        # if a module requires a custom setting, it can be stored here
        self.settings = {}
        self.settings_valid = False
        self.register_settings(self.app_name, {
            'company_name': forms.CharField(
                max_length=100,
                required=True,
            ),
            'company_email': forms.EmailField(
                required=True,
            ),
            # TODO add validation / use dropdown
            'currency': forms.CharField(
                max_length=10,
                required=True,
                initial=None,
            ),
        })

    def activate(self, test=False):

        if self.is_active or not test:  # pragma: no cover
            return True

        # ~~~~ numbercycles ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        for model in self.numbercycles:
            ct = ContentType.objects.get_for_model(model)
            count = NumberCycle.objects.filter(ct=ct).count()
            if not count:  # pragma: no branch
                obj = NumberCycle(ct=ct, name_template=model._bmfmeta.number_cycle)
                obj.save()
                logger.debug('Numbercycle for model %s created' % model.__class__.__name__)

        # ~~~~ END ~ activate ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.is_active = True
        return True

    # --- modules -------------------------------------------------------------

    def register_module(self, module, **options):
        if not hasattr(module, '_bmfmeta'):
            raise ImproperlyConfigured(
                'The module %s needs to be an BMF-Model in order to be'
                'registered with django BMF.' % module.__name__
            )
        if module in self.modules:
            raise AlreadyRegistered('The module %s is already registered' % module.__name__)
        self.modules[module] = Module(module, **options)

    def unregister_module(self, module):
        if module not in self.modules:
            raise NotRegistered('The model %s is not registered' % module.__name__)
        del self.modules[module]

    def get_module(self, module):
        return self.modules[module]

    # --- currencies ----------------------------------------------------------

    def register_currency(self, currency):
        if currency.iso in self.currencies:
            raise AlreadyRegistered('The currency %s is already registered' % currency.__name__)
        self.currencies[currency.iso] = currency

        # set the first registered currency as the initial one
        if len(self.currencies) == 1:
            self.get_setting_field("djangobmf", "currency").initial = currency.iso

    def unregister_currency(self, currency):
        if currency.iso not in self.currencies:
            raise NotRegistered('The currency %s is not registered' % currency.__name__)
        del self.currencies[currency.iso]

    # --- reports -------------------------------------------------------------

    def register_report(self, name, cls):
        if name in self.reports:
            raise AlreadyRegistered('The report %s is already registered' % name)
        self.reports[name] = cls

    def unregister_report(self, name):
        if name not in self.reports:
            raise NotRegistered('The currency %s is not registered' % name)
        del self.reports[name]

    # --- settings ------------------------------------------------------------

    def register_settings(self, app_label, settings_dict):
        for setting_name, field in settings_dict.items():
            self.register_setting(app_label, setting_name, field)

    def register_setting(self, app_label, setting_name, field):
        name = '.'.join([app_label, setting_name])
        if name in self.settings:
            raise AlreadyRegistered('The setting %s is already registered' % name)
        self.settings[name] = field

    def unregister_setting(self, app_label, setting_name):
        name = '.'.join([app_label, setting_name])
        if name not in self.settings:
            raise NotRegistered('The setting %s is not registered' % name)
        del self.settings[name]

    def get_setting_field(self, app_label, setting_name):
        name = '.'.join([app_label, setting_name])
        return self.settings[name]

    # --- number cycle --------------------------------------------------------

    def register_numbercycle(self, model):
        self.numbercycles.append(model)

    # --- dashboards ----------------------------------------------------------

    def register_dashboards(self, *args):
        for dashboard in args:
            if dashboard in self.dashboards:
                # merge
                i = self.dashboards.index(dashboard)
                self.dashboards[i].merge(dashboard)
            else:
                # append
                self.dashboards.append(dashboard)

    def get_dashboard(self, key):
        data = [i for i in self.dashboards if i.key == key]
        if len(data) == 1:
            return data[0]
        raise KeyError(key)

    # --- url generation ------------------------------------------------------

    # --- misc methods --------------------------------------------------------

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace

    @property
    def models(self):
        models = {}
        for model in self.modules.keys():
            ct = ContentType.objects.get_for_model(model)
            models[ct.pk] = model
        return models

    def get_urls(self):

        from djangobmf.urls import urlpatterns

        self.activate()

        for module, data in self.modules.items():
            info = (module._meta.app_label, module._meta.model_name)

            try:
                ct = ContentType.objects.get_for_model(module)
            except RuntimeError:
                # During the first migrate command, contenttypes are not ready
                # and raise a Runtime error. We ignore that error and return
                # an empty pattern - the urls are not needed during migrations.
                return patterns('')

            # set the apis
            urlpatterns += patterns(
                '',
                url(
                    r'^api/module/%s/' % ct.pk,
                    include((data.get_api_urls(), self.app_name, "moduleapi_%s_%s" % info))
                ),
            )

            # Skip detail view if the model is marked as a only related model
            if not module._bmfmeta.only_related:
                urlpatterns += patterns(
                    '',
                    url(
                        r'^detail/%s/%s/(?P<pk>[0-9]+)/' % (info[1], info[0]),
                        include((data.get_detail_urls(), self.app_name, "detail_%s_%s" % info))
                    ),
                )

        return urlpatterns
