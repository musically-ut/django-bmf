#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def get_url_from_ct(ct, pk):
    model = ct.model_class()
    if hasattr(model, '_bmfmeta'):
        return reverse('%s:detail' % model._bmfmeta.namespace_detail, kwargs={'pk': pk})
    return '#'


@register.simple_tag
def get_bmf_url(obj, view="detail", key="default", **kwargs):
    if hasattr(obj, '_bmfmeta'):

        if view in ["detail"]:
            namespace = obj._bmfmeta.namespace_detail
        else:
            namespace = obj._bmfmeta.namespace_api

        if view in ["detail", "update", "delete", "workflow", "report", "clone"]:
            kwargs.update({'pk': obj.pk})

        if view in ["create", "report"]:
            kwargs.update({'key': key})

        return reverse('%s:%s' % (namespace, view), kwargs=kwargs)
    return '#'
