#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.template import Context
from django.template.loader import select_template
from django.utils import six

from djangobmf.conf import settings
from djangobmf.sites import site
from djangobmf.sites import Report
from djangobmf.models import Document

import requests


if six.PY3:
    from configparser import RawConfigParser
else:
    from ConfigParser import RawConfigParser

try:
    from xhtml2pdf import pisa
    from io import BytesIO
    XHTML2PDF = True
except ImportError:
    XHTML2PDF = False


DEFAULT_OPTS = """
[layout]
size = A4
form = A
letter = True

[letter_page]
margin_left = 10mm
margin_bottom = 15mm
extra = true
extra_right = 10mm
extra_top = 40mm
pdf_background_pk = None

[pages]
margin_left = 10mm
margin_bottom = 15mm
margin_top = 20mm
footer_right = 10mm
footer_height = 10mm
pdf_background_pk = None
"""


class Xhtml2PdfReport(Report):

    def __init__(self, options):
        self.options = RawConfigParser(allow_no_value=True)
        self.options.read_string(options)

    def get_default_options(self):
        return DEFAULT_OPTS

    def render(self, request, context):
        model = context['bmfmodule']['model']._meta
        template_name = '%s/%s_htmlreport.html' % (model.app_label, model.model_name)

        pages_file = None
        letter_file = None

        if self.options.has_option('pages', 'pdf_background_pk'):
            if self.options.getint('pages', 'pdf_background_pk'):
                bg_pk = self.options.getint('pages', 'pdf_background_pk')
                try:
                    file = Document.objects.get(pk=bg_pk)
                    pages_file = ''.join(file.file.read().encode('base64').splitlines())
                except Document.DoesNotExist:
                    pass

        if self.options.has_option('letter_page', 'pdf_background_pk'):
            if self.options.getint('letter_page', 'pdf_background_pk'):
                bg_pk = self.options.getint('letter_page', 'pdf_background_pk')
                try:
                    file = Document.objects.get(pk=bg_pk)
                    letter_file = ''.join(file.file.read().encode('base64').splitlines())
                except Document.DoesNotExist:
                    pass

        options = {
            'template_name': template_name,

            'size': self.options.get('layout', 'size'),
            'form': self.options.get('layout', 'form'),
            'letter': self.options.getboolean('layout', 'letter'),

            'template_letter': letter_file,
            'template_pages': pages_file,

            #  'margin_left': self.cfg.getboolean('letter_page', 'margin_left'),
            #  'margin_bottom': self.cfg.getboolean('letter_page', 'margin_bottom'),
            'extra': self.options.getboolean('letter_page', 'extra'),
            #  'extra_right': self.cfg.getboolean('letter_page', 'extra_right'),
            #  'extra_top': self.cfg.getboolean('letter_page', 'extra_top'),

        }
        context['options'] = options

        template = select_template([template_name, 'djangobmf/report_html_base.html'])

        # pdf won't be in UTF-8
        html = template.render(Context(context)).encode("ISO-8859-1")

        if settings.REPORTING_SERVER:
            response = requests.post(
                settings.REPORTING_SERVER,
                data=html,
                timeout=5.0,
            )
            return 'pdf', 'application/pdf', response.content, True
        else:
            buffer = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html, buffer))
            pdf = buffer.getvalue()
            buffer.close()
            return 'pdf', 'application/pdf', pdf, True


if XHTML2PDF or settings.REPORTING_SERVER:
    site.register_report('xhtml2pdf', Xhtml2PdfReport)
