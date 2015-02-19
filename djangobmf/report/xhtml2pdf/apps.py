from __future__ import unicode_literals

from djangobmf.apps import ReportTemplate


class ReportConfig(ReportTemplate):
    name = 'djangobmf.report.xhtml2pdf'
    label = "xhtml2pdf"
