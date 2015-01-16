#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

# from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# from django.utils.translation import ugettext_lazy as _

from djangobmf.core import site_lazy


@python_2_unicode_compatible
class Dashboard(models.Model):
    key = models.CharField(
        max_length=100,
        null=True,
        blank=False,
        db_index=True,
        unique=True,
    )

    def __str__(self):
        if self.key:
            return self.key
        return "Root-Dashboard"

    def natural_key(self):
        return self.key

    def is_root(self):
        return not bool(self.key)

    def has_view(self):
        return self.key in [i.key for i in getattr(site_lazy(), 'dashboards', [])]

    class Meta:
        abstract = True
        ordering = ('key',)
