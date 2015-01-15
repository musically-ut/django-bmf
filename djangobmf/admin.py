#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Configuration
from .models import Dashboard
from .models import NumberCycle
from .models import Report
from .models import Workspace


admin.site.register(Configuration)
admin.site.register(Dashboard)
admin.site.register(NumberCycle)
admin.site.register(Report)


class WorkspaceAdmin(MPTTModelAdmin):
    list_display = ('slug', '__str__', 'ct', 'public', 'editable', 'url')

admin.site.register(Workspace, WorkspaceAdmin)
