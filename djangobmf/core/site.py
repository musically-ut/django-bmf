#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import forms
from django.apps import apps
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.admin.sites import NotRegistered
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import OperationalError
from django.db.utils import ProgrammingError

from djangobmf.categories import BaseDashboard
from djangobmf.categories import BaseCategory
from djangobmf.core.module import Module
from djangobmf.core.setting import Setting
from djangobmf.models import NumberCycle
from djangobmf.settings import APP_LABEL

import logging
logger = logging.getLogger(__name__)

SETTING_KEY = "%s.%s"


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
        self.register_settings(APP_LABEL, {
            'company_name': forms.CharField(max_length=100, required=True,),
            'company_email': forms.EmailField(required=True,),
            'currency': forms.CharField(max_length=10, required=True,),  # TODO add validation / use dropdown
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

        # ~~~~ dashboards ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        for dashboard in self.dashboards:

            workspace = apps.get_model(APP_LABEL, "Workspace")

            label = '%s.%s' % (dashboard.__module__, dashboard.__class__.__name__)

            d_obj, created = workspace.objects.get_or_create(module=label, level=0)

            if created or d_obj.slug != obj.slug or d_obj.url != dashboard.slug:
                d_obj.slug = dashboard.slug
                d_obj.url = dashboard.slug
                d_obj.editable = False
                d_obj.save()
                logger.debug('Dashboard %s registered or updated' % label)

            for category in dashboard:
                c_obj, created = workspace.objects \
                    .select_related('parent') \
                    .get_or_create(module=label, parent=d_obj)

                if created or c_obj.slug != category.slug or c_obj.url != c_obj.get_url():
                    c_obj.slug = category.slug
                    c_obj.editable = False
                    c_obj.update_url()
                    c_obj.save()
                    logger.debug('Category %s registered or updated' % label)

        # ~~~~ END ~ acticate ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

    # --- currencies ----------------------------------------------------------

    def register_currency(self, currency):
        if currency.iso in self.currencies:
            raise AlreadyRegistered('The currency %s is already registered' % currency.__name__)
        self.currencies[currency.iso] = currency

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

    # TODO move settings to cache backend!
    def register_settings(self, app_label, settings_dict):
        pass
        for setting_name, options in settings_dict.items():
            self.register_setting(app_label, setting_name, options)

    # TODO move settings to cache backend!
    def register_setting(self, app_label, setting_name, options):
        name = SETTING_KEY % (app_label, setting_name)
        if name in self.settings:
            raise AlreadyRegistered('The setting %s is already registered' % name)
        self.settings[name] = Setting(app_label, setting_name, options)

    # TODO move settings to cache backend!
    def unregister_setting(self, app_label, setting_name):
        name = SETTING_KEY % (app_label, setting_name)
        if name not in self.settings:
            raise NotRegistered('The setting %s is not registered' % name)
        del self.settings[name]

    # TODO move settings to cache backend!
    def check_settings(self):
        self.settings_valid = False
        for key, setting in self.settings:
            if not setting.value and setting.field.required:
                self.settings_valid = False
                return False
        return True

    # TODO move settings to cache backend!
    def get_lazy_setting(self, app_label, setting_name):
        """
        will allways return None, if the django apps are not ready
        """
        if apps.ready:
            return self.get_setting(app_label, setting_name)
        return None

    # TODO move settings to cache backend!
    def get_setting(self, app_label, setting_name):
        name = SETTING_KEY % (app_label, setting_name)
        try:
            return self.settings[name].value
        except KeyError:
            raise NotRegistered('The setting %s is not registered' % name)

    # --- number cycle --------------------------------------------------------

    def register_numbercycle(self, model):
        self.numbercycles.append(model)

    # --- workspace -----------------------------------------------------------

    def register_dashboards(self, *args):
        for dashboard in args:
            if dashboard in self.dashboards:
                # merge
                i = self.dashboards.index(dashboard)
                self.dashboards[i].merge(dashboard)
            else:
                # append
                self.dashboards.append(dashboard)

    def register_dashboard(self, dashboard):

        if isinstance(dashboard, BaseDashboard):
            obj = dashboard
        else:
            obj = dashboard()

        label = '%s.%s' % (obj.__module__, obj.__class__.__name__)
        workspace = apps.get_model(APP_LABEL, "Workspace")

        try:
            ws, created = workspace.objects.get_or_create(module=label, level=0)
        except (OperationalError, ProgrammingError, ImproperlyConfigured):
            logger.debug('Database not ready, skipping registration of Dashboard %s' % label)
            return False

        if created or ws.slug != obj.slug or ws.url != obj.slug:
            ws.slug = obj.slug
            ws.url = obj.slug
            ws.editable = False
            ws.save()
            logger.debug('Dashboard %s registered' % label)

        return True

    def register_category(self, dashboard, category):

        if isinstance(dashboard, BaseDashboard):
            parent = dashboard
        else:
            parent = dashboard()

        if isinstance(category, BaseCategory):
            obj = category
        else:
            obj = category()

        label = '%s.%s' % (obj.__module__, obj.__class__.__name__)
        parent_label = '%s.%s' % (parent.__module__, parent.__class__.__name__)
        workspace = apps.get_model(APP_LABEL, "Workspace")

        try:
            parent_workspace = workspace.objects.get(module=parent_label)
        except (OperationalError, ProgrammingError, ImproperlyConfigured):
            logger.debug('Database not ready, skipping registration of Category %s' % label)
            return False
        except workspace.DoesNotExist:
            logger.error('%s does not exist - skipping registration of Category %s' % (parent_label, label))
            return False

        ws, created = workspace.objects \
            .select_related('parent') \
            .get_or_create(module=label, parent=parent_workspace)

        if created or ws.slug != obj.slug or ws.url != ws.get_url():
            ws.slug = obj.slug
            ws.editable = False
            ws.update_url()
            ws.save()
            logger.debug('Category %s registered' % label)

        return True

    def register_view(self, model, category, view, **kwargs):

        parent = category()
        obj = view()
        label = '%s.%s' % (obj.__module__, obj.__class__.__name__)
        parent_label = '%s.%s' % (parent.__module__, parent.__class__.__name__)
        workspace = apps.get_model(APP_LABEL, "Workspace")

        try:
            parent_workspace = workspace.objects.get(module=parent_label)
        except (OperationalError, ProgrammingError, ImproperlyConfigured):
            logger.debug('Database not ready, skipping registration of View %s' % label)
            return False
        except workspace.DoesNotExist:
            logger.error('%s does not exist - skipping registration of View %s' % (parent_label, label))
            return False

        ct = ContentType.objects.get_for_model(model)

        ws, created = workspace.objects \
            .select_related('parent') \
            .get_or_create(module=label, parent=parent_workspace)

        if created or ws.slug != obj.slug or ws.url != ws.get_url() or ws.ct != ct:
            ws.ct = ct
            ws.slug = obj.slug
            ws.editable = False
            ws.update_url()
            ws.save()
            logger.debug('View %s registered' % label)

        return True

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
            ct = ContentType.objects.get_for_model(module)

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

#       # build dashboards
#       urlpatterns += patterns(
#           '',
#           url(
#               r'^workspace',
#               include((self.get_workspace_urls(), self.app_name, "workspace"))
#           ),
#       )

        return urlpatterns
