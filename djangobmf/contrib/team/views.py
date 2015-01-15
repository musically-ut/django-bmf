#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetailView
from djangobmf.views import ModuleListView

from .forms import TeamUpdateForm
from .forms import TeamCreateForm


class TeamIndexView(ModuleListView):
    name = _("All Teams")
    slug = "all"


class TeamCreateView(ModuleCreateView):
    form_class = TeamCreateForm


class TeamUpdateView(ModuleUpdateView):
    form_class = TeamUpdateForm


class TeamDetailView(ModuleDetailView):
    pass
