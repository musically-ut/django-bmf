#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.core.cache import caches
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djangobmf.settings import CACHE_DEFAULT_CONNECTION

import json


CACHE_KEY_TEMPLATE = 'bmfconfig.%s.%s'


class ConfigurationManager(models.Manager):

    def get_setting(self, app, name):
        """
        Returns the current ``Configuration`` based on the app-label and
        the name of the setting. The ``Configuration`` object is cached in the
        bmf default cache connection (which should be shared throughout all instances)
        """
        # We need a database connection, and thus the apps to be ready
        if not apps.ready:
            return None

        cache = caches[CACHE_DEFAULT_CONNECTION]
        key = CACHE_KEY_TEMPLATE % (app, name)
        value = cache.get(key)

        if not value:
            object, created = self.get_or_create(app_label=app, field_name=name)

            if created:
                from djangobmf.sites import site

                try:
                    field = site.get_setting_field(app, name)
                except KeyError:
                    object.delete()
                    raise

                object.value = json.dumps(field.initial)
                value = field.initial

            else:
                value = json.loads(object.value)

            cache.set(key, value)

        return value


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

    objects = ConfigurationManager()

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')
        default_permissions = ('change',)
        abstract = True

    def remove_cached_value(self):
        """
        removes the cache key to ensure it is reloaded if needed
        """
        cache = caches[CACHE_DEFAULT_CONNECTION]
        key = CACHE_KEY_TEMPLATE % (self.app_label, self.field_name)
        cache.delete(key)

    def save(self, *args, **kwargs):
        super(Configuration, self).save(*args, **kwargs)
        # Cached information will likely be incorrect now.
        self.remove_cached_value()

    def delete(self):
        super(Configuration, self).delete()
        # Cached information will likely be incorrect now.
        self.remove_cached_value()

    @classmethod
    def get_setting(cls, app, name):
        return cls._default_manager.get_setting(app, name)

    def __str__(self):
        return '%s.%s' % (self.app_label, self.field_name)

    @models.permalink
    def get_absolute_url(self):
        return ('djangobmf:configuration', (), {
            "app_label": self.app_label,
            "name": self.field_name,
        })

#   def clear_cache(self):
#       """Clears the ``Configuration`` object cache."""
#       cache = caches[CACHE_DEFAULT_CONNECTION]
#       cache.clear()
