#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from django.utils.six import with_metaclass

from djangobmf.currency import BaseCurrency

from .workflow import WorkflowField


__all__ = [
    'OLDWorkflowField',
    'WorkflowField',
    'CurrencyField',
    'MoneyField',
]


class OLDWorkflowField(with_metaclass(models.SubfieldBase, models.CharField)):
    """
    OLD DONT USE
    """
    description = "Workflow field"

    def __init__(self, **kwargs):
        # TODO ADD REMOVAL WARNING
        defaults = {
            'max_length': 32,  # max length
            'db_index': True,
        }
        defaults.update(kwargs)
        defaults.update({
            'null': True,
            'blank': True,
            'editable': False,
        })
        super(OLDWorkflowField, self).__init__(**defaults)


# Currency and Money
# -----------------------------------------------------------------------------
# see: http://blog.elsdoerfer.name/2008/01/08/fuzzydates-or-one-django-model-field-multiple-database-columns/


def get_default_currency():
    from djangobmf.models import Configuration
    return Configuration.get_setting('djangobmf', 'currency')


class MoneyProxy(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):

        # get currency model
        currency = getattr(obj, self.field.get_currency_field_name())

        if self.field.has_precision:
            precision = getattr(obj, self.field.get_precision_field_name())
        else:
            precision = 0

        if currency and not isinstance(value, BaseCurrency):
            value = currency.__class__(value, precision=precision)

        obj.__dict__[self.field.name] = value


class CurrencyField(with_metaclass(models.SubfieldBase, models.CharField)):
    description = _("Currency Field")

    def __init__(self, *args, **kwargs):
        defaults = {
            'max_length': 4,
            'editable': False,
        }
        defaults.update(kwargs)
        defaults.update({
            'null': True,
            'blank': False,
            'default': get_default_currency,
        })
        super(CurrencyField, self).__init__(*args, **defaults)

    def to_python(self, value):
        if isinstance(value, BaseCurrency):
            return value

        elif not value:
            return None

        # The string case.
        try:
            from .sites import site
            return site.currencies['%s' % value]()
        except ImportError:
            return None

    def get_prep_value(self, obj):
        if hasattr(obj, 'iso'):
            return obj.iso
        return None

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def deconstruct(self):
        name, path, args, kwargs = super(CurrencyField, self).deconstruct()
        del kwargs["null"]
        del kwargs["default"]
        return name, path, args, kwargs


class MoneyField(models.DecimalField):
    description = _("Money Field")

    def __init__(self, *args, **kwargs):
        defaults = {
            'default': None,
            'blank': True,
        }
        defaults.update(kwargs)
        defaults.update({
            'null': True,
            'max_digits': 27,
            'decimal_places': 9,
        })
        super(MoneyField, self).__init__(*args, **defaults)

    def to_python(self, value):
        if isinstance(value, BaseCurrency):
            return value.value
        return super(MoneyField, self).to_python(value)

    def get_currency_field_name(self):
        return '%s_currency' % self.name

    def get_precision_field_name(self):
        return '%s_precision' % self.name

    def deconstruct(self):
        name, path, args, kwargs = super(MoneyField, self).deconstruct()
        del kwargs["null"]
        del kwargs["max_digits"]
        del kwargs["decimal_places"]
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name):
        super(MoneyField, self).contribute_to_class(cls, name)
        if not cls._meta.abstract:
            self.has_precision = hasattr(self, self.get_precision_field_name())
            setattr(cls, self.name, MoneyProxy(self))

    def formfield(self, **kwargs):
        kwargs.update({
            'widget': TextInput,
        })
        value = super(MoneyField, self).formfield(**kwargs)
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        if isinstance(value, BaseCurrency):
            value = value.value
        super(MoneyField, self).get_prep_value(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        if isinstance(value, BaseCurrency):
            value = value.value
        return super(MoneyField, self).get_db_prep_save(value, *args, **kwargs)


'''
#-*- coding: utf-8 -*-
import inspect
from django import forms
from django.conf import settings as globalsettings
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.contrib.admin.sites import site
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from filer.utils.compatibility import truncate_words
from filer.models import File
from filer import settings as filer_settings

import logging
logger = logging.getLogger(__name__)

class AdminFileFormField(forms.ModelChoiceField):
    widget = AdminFileWidget

    def __init__(self, rel, queryset, to_field_name, *args, **kwargs):
        self.rel = rel
        self.queryset = queryset
        self.to_field_name = to_field_name
        self.max_value = None
        self.min_value = None
        other_widget = kwargs.pop('widget', None)
        if 'admin_site' in inspect.getargspec(self.widget.__init__)[0]: # Django 1.4
            widget_instance = self.widget(rel, site)
        else: # Django <= 1.3
            widget_instance = self.widget(rel)
        forms.Field.__init__(self, widget=widget_instance, *args, **kwargs)

    def widget_attrs(self, widget):
        widget.required = self.required
        return {}


class FilerFileField(models.ForeignKey):
    default_form_class = AdminFileFormField
    default_model_class = File

    def __init__(self, **kwargs):
        # we call ForeignKey.__init__ with the Image model as parameter...
        # a FilerImageFiled can only be a ForeignKey to a Image
        return super(FilerFileField, self).__init__(
            self.default_model_class, **kwargs)

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {
            'form_class': self.default_form_class,
            'rel': self.rel,
        }
        defaults.update(kwargs)
        return super(FilerFileField, self).formfield(**defaults)

from datetime import date
from django.forms import widgets

from django.contrib.admin.widgets import ForeignKeyRawIdWidget

'''
