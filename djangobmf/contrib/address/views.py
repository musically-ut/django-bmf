#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleListView


class AddressIndexView(ModuleListView):
    name = _("All Addresses")
    slug = "all"
