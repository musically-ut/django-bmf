#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleGetView


class ProjectGetView(ModuleGetView):
    def get_item_data(self, data):
        l = []
        for d in data:
            customer = d.bmfget_customer()
            l.append({
                'name': str(d),
                'is_active': d.is_active,
                'customer': '%s' % customer if customer else '',
                'url': d.bmfmodule_detail(),
            })
        return l


class ProjectUpdateView(ModuleUpdateView):
    pass
