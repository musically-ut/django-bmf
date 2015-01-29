#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.core.cache import caches
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djangobmf.settings import CACHE_DEFAULT_CONNECTION

import json


@python_2_unicode_compatible
class Configuration(models.Model):
    """
    Model to store informations about settings
    """

    app_label = models.CharField(
        _("Application"), max_length=100, editable=False, null=True, blank=False,
    )
    field_name = models.CharField(
        _("Fieldname"), max_length=100, editable=False, null=True, blank=False,
    )
    value = models.TextField(_("Value"), null=True, blank=False)

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')
        default_permissions = ('change',)
        abstract = True

    def get_key(self):
        return 'bmfconfig.%s.%s' % (self.app_label, self.field_name)

    def get_cache(self):
        return caches[CACHE_DEFAULT_CONNECTION]

    def get_value(self):
        """
        Returns the current ``Configuration`` based on the app-label and
        the name of the setting. The ``Configuration`` object is cached in the
        bmf default cache connection (which should be shared throughout all instances)
        """
        cache = self.get_cache()
        key = self.get_key()

        value = cache.get(key)

        if not value:
            value = json.loads(self.value)
            cache.set(key, value)

        return value

    def remove_value(self):
        """
        removes the cache key to ensure it is reloaded if needed
        """
        cache = self.get_cache()
        key = self.get_key()
        cache.delete(key)

    def clear_cache(self):
        """Clears the ``Configuration`` object cache."""
        cache = caches[CACHE_DEFAULT_CONNECTION]
        cache.clear()

    def save(self, *args, **kwargs):
        super(Configuration, self).save(*args, **kwargs)
        # Cached information will likely be incorrect now.
        self.remove_value()

    def delete(self):
        super(Configuration, self).delete()
        # Cached information will likely be incorrect now.
        self.remove_value()

    def __str__(self):
        return '%s.%s' % (self.app_label, self.field_name)

    @models.permalink
    def get_absolute_url(self):
        return ('djangobmf:configuration', (), {
            "app_label": self.app_label,
            "name": self.field_name,
        })
