#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from .mixins import ViewMixin


class ModuleOverviewView(ViewMixin, TemplateView):
    template_name = "djangobmf/modules.html"

    def get_context_data(self, **kwargs):
        from djangobmf.sites import site

        modules = []
        for ct, model in site.models.items():
            info = model._meta.app_label, model._meta.model_name
            perm = '%s.view_%s' % info
            if not model._bmfmeta.only_related and self.request.user.has_perms([perm]):  # pragma: no branch
                modules.append({
                    'model': model,
                    'url': reverse('%s:list' % model._bmfmeta.namespace_api),
                    'name': model._meta.verbose_name_plural,
                })

        context = super(ModuleOverviewView, self).get_context_data(**kwargs)
        context['modules'] = modules
        context['workspaces'] = site.dashboards
        return context
