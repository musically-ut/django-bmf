#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.sites import site

from .models import Team
from .models import TeamMember

from .views import TeamCreateView
from .views import TeamDetailView
from .views import TeamUpdateView


site.register_module(Team, **{
    'create': TeamCreateView,
    'detail': TeamDetailView,
    'update': TeamUpdateView,
})

site.register_module(TeamMember, **{
})
