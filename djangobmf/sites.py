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
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import OperationalError
from django.db.utils import ProgrammingError
from django.utils.module_loading import module_has_submodule
from django.utils.module_loading import import_module
from django.utils import six
from django.utils.text import slugify

from .apps import BMFConfig
from .models import Configuration
from .views import ModuleCloneView
from .views import ModuleCreateView
from .views import ModuleDeleteView
from .views import ModuleDetailView
from .views import ModuleFormAPI
from .views import ModuleGetView
from .views import ModuleListView
from .views import ModuleReportView
from .views import ModuleUpdateView
from .views import ModuleWorkflowView

import copy
import sys

import logging
logger = logging.getLogger(__name__)

SETTING_KEY = "%s.%s"
APP_LABEL = BMFConfig.label


class DjangoBMFSetting(object):
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


class DjangoBMFModule(object):
    """
    Object internally used to register modules
    """

    def __init__(self, model, **options):
        self.model = model

        self.create = options.get('create', ModuleCreateView)
        self.detail = options.get('detail', ModuleDetailView)
        self.update = options.get('update', ModuleUpdateView)
        self.delete = options.get('delete', ModuleDeleteView)
        self.clone = options.get('clone', ModuleCloneView)
        self.get = options.get('get', ModuleGetView)
        self.report = options.get('report', None)
        self.detail_urlpatterns = options.get('detail_urlpatterns', None)
        self.api_urlpatterns = options.get('api_urlpatterns', None)

    def list_reports(self):
        if hasattr(self, 'listed_reports'):
            return self.listed_reports
        self.listed_reports = []

        if isinstance(self.report, dict):
            for label, view in six.iteritems(self.report):
                key = slugify(label)
                if isinstance(view, (list, tuple)) and len(view) == 2:
                    # overwrite the label, and correct the view
                    label = slugify(view[0])
                    view = view[1]
            self.listed_reports.append((key, label, view))

        elif isinstance(self.report, bool):
            self.listed_reports.append(('default', 'default', ModuleReportView))
        elif self.report and issubclass(self.report, ModuleReportView):
            self.listed_reports.append(('default', 'default', self.report))

        return self.listed_reports

    def list_creates(self):
        if hasattr(self, 'listed_creates'):
            return self.listed_creates
        self.listed_creates = []

        if isinstance(self.create, dict):
            for label, view in six.iteritems(self.create):
                key = slugify(label)

                if isinstance(view, (list, tuple)) and len(view) == 2:
                    # overwrite the label, and use the correct the view function
                    label = view[0]
                    view = view[1]
                self.listed_creates.append((key, label, view))

        elif issubclass(self.create, ModuleCreateView):
            self.listed_creates.append(('default', 'default', self.create))

        # update model with all create views
        self.model._bmfmeta.create_views = self.listed_creates

        return self.listed_creates

    def get_detail_urls(self):
        reports = self.list_reports()

        urlpatterns = patterns(
            '',
            url(
                r'^$',
                self.detail.as_view(model=self.model, reports=reports),
                name='detail',
            ),
        )

        # add custom url patterns
        if self.detail_urlpatterns:
            urlpatterns += self.detail_urlpatterns

        return urlpatterns

    def get_api_urls(self):
        reports = self.list_reports()
        creates = self.list_creates()

        urlpatterns = patterns(
            '',
            url(
                r'^$',
                ModuleListView.as_view(model=self.model),
                name='list',
            ),
            url(
                r'^get/$',
                self.get.as_view(model=self.model),
                name='get',
            ),
            url(
                r'^update/(?P<pk>[0-9]+)/$',
                self.update.as_view(model=self.model),
                name='update',
            ),
            url(
                r'^update/(?P<pk>[0-9]+)/form/$',
                ModuleFormAPI.as_view(
                    model=self.model,
                    form_view=self.update,
                ),
                name='update-form',
            ),
            url(
                r'^delete/(?P<pk>[0-9]+)/$',
                self.delete.as_view(model=self.model),
                name='delete',
            ),
        )
        if self.model._bmfmeta.can_clone:
            urlpatterns += patterns(
                '',
                url(
                    r'^clone/(?P<pk>[0-9]+)/$',
                    self.clone.as_view(model=self.model),
                    name='clone',
                ),
                url(
                    r'^clone/(?P<pk>[0-9]+)/form/$',
                    ModuleFormAPI.as_view(
                        model=self.model,
                        form_view=self.clone,
                    ),
                    name='clone-form',
                ),
            )

        for key, label, view in creates:
            urlpatterns += patterns(
                '',
                url(
                    r'^create/(?P<key>%s)/$' % key,
                    view.as_view(model=self.model),
                    name='create',
                ),
                url(
                    r'^create/(?P<key>%s)/form/$' % key,
                    ModuleFormAPI.as_view(
                        model=self.model,
                        form_view=view,
                    ),
                    name='create-form',
                ),
            )

        for key, label, view in reports:
            urlpatterns += patterns(
                '',
                url(
                    r'^report/(?P<key>%s)/$' % key,
                    view.as_view(model=self.model),
                    name='report',
                ),
            )

        # workflow interactions
        if bool(len(self.model._bmfworkflow._transitions)):
            urlpatterns += patterns(
                '',
                url(
                    r'^workflow/(?P<pk>[0-9]+)/(?P<transition>\w+)/$',
                    ModuleWorkflowView.as_view(model=self.model),
                    name='workflow',
                ),
            )

        # add custom url patterns
        if self.api_urlpatterns:
            urlpatterns += self.api_urlpatterns

        return urlpatterns


class DjangoBMFSite(object):
    """
    Handle modules like the AdminSite from django.contrib.admin.sites
    """

    def __init__(self, name='djangobmf', app_name=APP_LABEL):
        self.name = name
        self.app_name = app_name
        self.clear()

    def clear(self):
        # combine all registered modules here
        self.modules = {}

        # all currencies should be stored here
        self.currencies = {}

        # all reports should be stored here
        self.reports = {}

        # if a module requires a custom setting, it can be stored here
        self.settings = {}
        self.settings_valid = False
        self.register_settings(APP_LABEL, {
            'company_name': forms.CharField(max_length=100, required=True,),
            'company_email': forms.EmailField(required=True,),
            'currency': forms.CharField(max_length=10, required=True,),  # TODO add validation / use dropdown
        })

    # --- modules -------------------------------------------------------------

    def register_module(self, module, **options):
        if not hasattr(module, '_bmfmeta'):
            raise ImproperlyConfigured(
                'The module %s needs to be an BMF-Model in order to be'
                'registered with django BMF.' % module.__name__
            )
        if module in self.modules:
            raise AlreadyRegistered('The module %s is already registered' % module.__name__)
        self.modules[module] = DjangoBMFModule(module, **options)
        logger.debug('registered module %s' % module.__name__)

    def unregister_module(self, module):
        if module not in self.modules:
            raise NotRegistered('The model %s is not registered' % module.__name__)
        del self.modules[module]
        logger.debug('deleted module %s' % module.__name__)

    # --- models --------------------------------------------------------------

    # TODO REMOVE ME
    def register(self, module, **options):
        self.register_module(module, **options)

    # TODO REMOVE ME
    def unregister(self, module):
        self.unregister_model(module)

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
        for setting_name, options in settings_dict.items():
            self.register_setting(app_label, setting_name, options)

    # TODO move settings to cache backend!
    def register_setting(self, app_label, setting_name, options):
        name = SETTING_KEY % (app_label, setting_name)
        if name in self.settings:
            raise AlreadyRegistered('The setting %s is already registered' % name)
        self.settings[name] = DjangoBMFSetting(app_label, setting_name, options)

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

    # --- workspace -----------------------------------------------------------

    def register_dashboard(self, dashboard):

        obj = dashboard()
        label = '%s.%s' % (obj.__module__, obj.__class__.__name__)
        workspace = apps.get_model(APP_LABEL, "Workspace")

        try:
            ws, created = workspace.objects.get_or_create(module=label, level=0)
        except (OperationalError, ProgrammingError):
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

        parent = dashboard()
        obj = category()
        label = '%s.%s' % (obj.__module__, obj.__class__.__name__)
        parent_label = '%s.%s' % (parent.__module__, parent.__class__.__name__)
        workspace = apps.get_model(APP_LABEL, "Workspace")

        try:
            parent_workspace = workspace.objects.get(module=parent_label)
        except (OperationalError, ProgrammingError):
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

    def register_view(self, model, category, view):

        parent = category()
        obj = view()
        label = '%s.%s' % (obj.__module__, obj.__class__.__name__)
        parent_label = '%s.%s' % (parent.__module__, parent.__class__.__name__)
        workspace = apps.get_model(APP_LABEL, "Workspace")

        try:
            parent_workspace = workspace.objects.get(module=parent_label)
        except (OperationalError, ProgrammingError):
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

    # --- misc methods --------------------------------------------------------

    @property
    def is_ready(self):
        return apps.get_app_config(APP_LABEL).is_ready

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name

    @property
    def models(self):
        models = {}
        for model in self.modules.keys():
            ct = ContentType.objects.get_for_model(model)
            models[ct.pk] = model
        return models

    def check_dependencies(self):
        """
        Check that all things needed to run the admin have been correctly installed.

        The default implementation checks that admin and contenttypes apps are
        installed, as well as the auth context processor.
        """
        # TODO: Check out django's system checks framework and redo checks
        # https://docs.djangoproject.com/en/1.7/topics/checks/
        if not apps.is_installed('django.contrib.admin'):
            raise ImproperlyConfigured(
                "Put 'django.contrib.admin' in "
                "your INSTALLED_APPS setting in order to use the bmf."
            )
        if not apps.is_installed('django.contrib.contenttypes'):
            raise ImproperlyConfigured(
                "Put 'django.contrib.contenttypes' in "
                "your INSTALLED_APPS setting in order to use the bmf."
            )
        if 'django.contrib.auth.context_processors.auth' not in settings.TEMPLATE_CONTEXT_PROCESSORS:
            raise ImproperlyConfigured(
                "Put 'django.contrib.auth.context_processors.auth' "
                "in your TEMPLATE_CONTEXT_PROCESSORS setting in order to use the bmf."
            )

    def get_urls(self):
        from djangobmf.urls import urlpatterns
        if not apps.ready and "migrate" in sys.argv:
            return urlpatterns

        if settings.DEBUG:
            self.check_dependencies()

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
        return urlpatterns


def autodiscover():
    for app_config in apps.get_app_configs():
        try:
            # get a copy of old site configuration
            before_import_m = copy.copy(site.modules)
            before_import_c = copy.copy(site.currencies)
            before_import_s = copy.copy(site.settings)
            before_import_p = copy.copy(site.reports)
            import_module('%s.%s' % (app_config.name, "bmf_module"))
            logger.debug('bmf_module from %s loaded' % app_config.name)
        except:
            # Reset the model registry to the state before the last import
            # skiping this may result in an AlreadyRegistered Error
            site.modules = before_import_m
            site.currencies = before_import_c
            site.settings = before_import_s
            site.reports = before_import_p

            # Decide whether to bubble up this error
            if module_has_submodule(app_config.module, "bmf_module"):
                raise

site = DjangoBMFSite()
