#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from djangobmf.models import BMFModel
from djangobmf.settings import CONTRIB_EMPLOYEE
from djangobmf.settings import CONTRIB_PROJECT
from djangobmf.settings import CONTRIB_INVOICE
from djangobmf.settings import CONTRIB_PRODUCT
from djangobmf.fields import CurrencyField
from djangobmf.fields import MoneyField


RATE_CHOICES = (
    (1, '100%'),
    (2, '80%'),
    (3, '50%'),
    (4, '0%'),
)


class PositionManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(PositionManager, self).get_queryset(*args, **kwargs) \
            .select_related('project', 'product', 'employee')

    def open(self, request):
        return self.get_queryset().filter(
            invoice__isnull=True,
        )


@python_2_unicode_compatible
class AbstractPosition(BMFModel):
    """
    """
    project = models.ForeignKey(  # TODO: make optional
        CONTRIB_PROJECT, null=True, blank=False,
        related_name="+", on_delete=models.SET_NULL,
    )
    employee = models.ForeignKey(  # TODO: make optional
        CONTRIB_EMPLOYEE, null=True, blank=False, on_delete=models.SET_NULL,
    )

    date = models.DateField(_("Date"), null=True, blank=False)
    name = models.CharField(_("Name"), max_length=255, null=True, blank=False)
    invoice = models.ForeignKey(
        CONTRIB_INVOICE, null=True, blank=True, related_name="+",
        editable=False, on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        CONTRIB_PRODUCT, null=True, blank=False, on_delete=models.PROTECT,
    )

    invoiceable = models.PositiveSmallIntegerField(
        _("Invoiceable"), null=True, blank=False, default=1, choices=RATE_CHOICES, editable=False,
    )
    price_currency = CurrencyField()
    price_precision = models.PositiveSmallIntegerField(default=0, blank=True, null=True, editable=False)
    price = MoneyField(_("Price"), blank=False)
    amount = models.FloatField(_("Amount"), null=True, blank=False, default=1.0)
    description = models.TextField(_("Description"), null=True, blank=True)

    objects = PositionManager()

    def __str__(self):
        return '%s' % (self.name)

    def has_invoice(self):
        return bool(self.invoice)

    def bmfget_customer(self):
        if hasattr(self, 'project'):
            return self.project.customer
        else:
            return None

    def bmfget_project(self):
        if hasattr(self, 'project'):
            return self.project
        else:
            return None

    def clean(self):
        if self.product and not self.name:
            self.name = self.product.name
        if self.product and not self.price:
            self.price = self.product.price

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')
        abstract = True
        swappable = "BMF_CONTRIB_POSITION"

    class BMFMeta:
        has_logging = False


class Position(AbstractPosition):
    pass
