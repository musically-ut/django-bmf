#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.http import HttpResponse

from djangobmf.core.report import Report as BaseReport


class Report(models.Model):
    """
    Model to store informations to generate a report
    """
    key = models.CharField(
        _("Key"), max_length=50, blank=False, null=False, editable=False, db_index=True,
    )
    # TODO OLD
    reporttype = models.CharField(
        _("Reporttype"), max_length=20, blank=False, null=False,
    )
    # TODO OLD
    mimetype = models.CharField(
        _("Mimetype"), max_length=20, blank=False, null=False, editable=False, default="pdf",
    )

    contenttype = models.ForeignKey(
        ContentType, related_name="bmf_report", null=True, blank=True,
        help_text="Connect a Report to an BMF-Model", on_delete=models.CASCADE,
    )

    renderer_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    renderer_id = models.PositiveIntegerField(null=True)
    renderer_object = GenericForeignKey('renderer_ct', 'renderer_id')

    is_active = models.BooleanField(_("Is active"), default=True, editable=False)
    has_object = models.BooleanField(_("Has object"), default=True, editable=False, db_index=True)

    options = models.TextField(
        _("Options"), blank=True, null=False,
        help_text=_(
            "Options for the renderer. Gets synced with the renderers options"
        ),
    )
    modified = models.DateTimeField(_("Modified"), auto_now=True, editable=False,)

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        get_latest_by = "modified"
        abstract = True
        unique_together = (('key', 'contenttype', 'has_object'),)

    def __str__(self):
        return '%s (%s)' % (self.contenttype, self.key)

    def clean(self):
        if self.options == "":
            generator = self.get_generator()
            self.options = generator.get_default_options().strip()

    def get_generator(self):
        from djangobmf.sites import site
        try:
            return site.reports[self.reporttype](self.options)
        except KeyError:
            return BaseReport()

    # response with generated file
    def render(self, filename, request, context):
        generator = self.get_generator()

        extension, mimetype, data, attachment = generator.render(request, context)

        response = HttpResponse(content_type=mimetype)

        if attachment:
            response['Content-Disposition'] = 'attachment; filename="%s.%s"' % (
                filename,
                extension
            )

        response.write(data)

        return response
