#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory


class ProjectCategory(BaseCategory):
    name = _('Projects')
    slug = "projects"
