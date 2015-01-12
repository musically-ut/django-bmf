#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleListView

class WorkspaceTestView(ModuleListView):
    slug = "test"
    name = "test"
