#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.template import Context
from django.template.loader import select_template


class Report(object):

    def __init__(self, options=None):
        self.options = options

    def get_default_options(self):
        return ''

    def render(self, request, context):
        """
        Dummy render function, reads a template and renders it as html

        returns extension, mime_type, data or file_object, attachment-boolean
        """
        model = context['bmfmodule']['model']._meta
        template_name = '%s/%s_htmlreport.html' % (model.app_label, model.model_name)
        template = select_template([template_name, 'djangobmf/report_html_base.html'])
        return 'html', 'text/html', template.render(Context()), False
