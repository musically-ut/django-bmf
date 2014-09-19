#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleLetterView


class ActiveProjectView(ModuleLetterView):
    slug = "active"
    name = _("Active Projects")


class AllProjectView(ModuleLetterView):
    slug = "all"
    name = _("All Projects")


class ProjectUpdateView(ModuleUpdateView):
    pass
