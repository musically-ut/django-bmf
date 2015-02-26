#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from djangobmf.conf import settings as bmfsettings
from djangobmf.document.storage import BMFStorage

from djangobmf.utils.generate_filename import generate_filename


@python_2_unicode_compatible
class Document(models.Model):
    name = models.CharField(_('Name'), max_length=120, null=True, blank=True, editable=False)
    file = models.FileField(_('File'), upload_to=generate_filename, storage=BMFStorage())
    size = models.PositiveIntegerField(null=True, blank=True, editable=False)
    mimetype = models.CharField(_('Mimetype'), max_length=50, editable=False, null=True)
    # sha1 = models.CharField(_('Mimetype'), max_length=40, editable=False, null=True)

    is_static = models.BooleanField(default=False)

    customer = models.ForeignKey(
        bmfsettings.CONTRIB_CUSTOMER,
        null=True,
        blank=True,
        related_name="documents",
        on_delete=models.SET_NULL,
    )

    project = models.ForeignKey(
        bmfsettings.CONTRIB_PROJECT,
        null=True,
        blank=True,
        related_name="documents",
        on_delete=models.SET_NULL,
    )

    content_type = models.ForeignKey(
        ContentType,
        related_name="bmf_document",
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    content_id = models.PositiveIntegerField(null=True, blank=True, editable=False)
    content_object = GenericForeignKey('content_type', 'content_id')

    modified = models.DateTimeField(_("Modified"), auto_now=True, editable=False, null=True, blank=False)
    created = models.DateTimeField(_("Created"), auto_now_add=True, editable=False, null=True, blank=False)
    modified_by = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        null=True, blank=True, editable=False,
        related_name="+", on_delete=models.SET_NULL)
    created_by = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        null=True, blank=True, editable=False,
        related_name="+", on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        get_latest_by = "modified"
        abstract = True

    def __str__(self):
        return self.name

    def clean(self):
        if self.file:
            self.size = self.file.size
            self.mimetype = self.file.content_type

        # import hashlib
        # f = self.image_file.open('rb')
        # hash = hashlib.sha1()
        # if f.multiple_chunks():
        # for chunk in f.chunks():
        #     hash.update(chunk)
        # else:    
        #     hash.update(f.read())
        # f.close()
        # self.sha1 =  hash.hexdigest()

        if not self.name:
            self.name = self.file.name.split(r'/')[-1]

        if hasattr(self, 'project') and hasattr(self.content_object, 'bmfget_project'):
            self.project_pk = getattr(self.content_object.bmfget_project(), 'pk', None)

        if hasattr(self, 'customer') and hasattr(self.content_object, 'bmfget_customer'):
            self.customer_pk = getattr(self.content_object.bmfget_customer(), 'pk', None)

    @models.permalink
    def bmffile_download(self):
        """
        A permalink to the default view of this model in the BMF-System
        """
        return ('djangobmf:document-get', (), {"pk": self.pk})
