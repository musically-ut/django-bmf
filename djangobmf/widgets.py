#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

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

class AdminFileWidget(ForeignKeyRawIdWidget):
    choices = None

    def render(self, name, value, attrs=None):
        obj = self.obj_for_value(value)
        css_id = attrs.get('id', 'id_image_x')
        css_id_thumbnail_img = "%s_thumbnail_img" % css_id
        css_id_description_txt = "%s_description_txt" % css_id
        related_url = None
        if value:
            try:
                file_obj = File.objects.get(pk=value)
                related_url = file_obj.logical_folder.\
                                get_admin_directory_listing_url_path()
            except Exception,e:
                # catch exception and manage it. We can re-raise it for debugging
                # purposes and/or just logging it, provided user configured
                # proper logging configuration
                if filer_settings.FILER_ENABLE_LOGGING:
                    logger.error('Error while rendering file widget: %s',e)
                if filer_settings.FILER_DEBUG:
                    raise
        if not related_url:
            related_url = reverse('admin:filer-directory_listing-last')
        params = self.url_parameters()
        if params:
            lookup_url = '?' + '&amp;'.join(
                                ['%s=%s' % (k, v) for k, v in params.items()])
        else:
            lookup_url = ''
        if not 'class' in attrs:
            # The JavaScript looks for this hook.
            attrs['class'] = 'vForeignKeyRawIdAdminField'
        # rendering the super for ForeignKeyRawIdWidget on purpose here because
        # we only need the input and none of the other stuff that
        # ForeignKeyRawIdWidget adds
        hidden_input = super(ForeignKeyRawIdWidget, self).render(
                                                            name, value, attrs)
        filer_static_prefix = filer_settings.FILER_STATICMEDIA_PREFIX
        if not filer_static_prefix[-1] == '/':
            filer_static_prefix += '/'
        context = {
            'hidden_input': hidden_input,
            'lookup_url': '%s%s' % (related_url, lookup_url),
            'thumb_id': css_id_thumbnail_img,
            'span_id': css_id_description_txt,
            'object': obj,
            'lookup_name': name,
            'filer_static_prefix': filer_static_prefix,
            'clear_id': '%s_clear' % css_id,
            'id': css_id,
        }
        html = render_to_string('admin/filer/widgets/admin_file.html', context)
        return mark_safe(html)

    def label_for_value(self, value):
        obj = self.obj_for_value(value)
        return '&nbsp;<strong>%s</strong>' % truncate_words(obj, 14)

    def obj_for_value(self, value):
        try:
            key = self.rel.get_related_field().name
            obj = self.rel.to._default_manager.get(**{key: value})
        except:
            obj = None
        return obj

    class Media:
        js = (filer_settings.FILER_STATICMEDIA_PREFIX + 'js/popup_handling.js',)


class FileWidget(widgets.MultiWidget):
  def __init__(self, attrs=None):

    _widgets = (
#     widgets.HiddenInput(attrs=attrs),
      widgets.TextInput(attrs=attrs),
      widgets.ClearableFileInput(attrs=attrs),
    )
    super(FileWidget, self).__init__(_widgets, attrs)

  def decompress(self, value):
    if value:
      return [value.day, value.year]
    return [None, None]

  def format_output(self, rendered_widgets):
    return u''.join(rendered_widgets)

  def value_from_datadict(self, data, files, name):
    datelist = [
      widget.value_from_datadict(data, files, name + '_%s' % i)
      for i, widget in enumerate(self.widgets)]
    try:
      D = date(day=int(datelist[0]), month=int(datelist[1]),
        year=int(datelist[2]))
    except ValueError:
      return ''
    else:
      return str(D)

'''
