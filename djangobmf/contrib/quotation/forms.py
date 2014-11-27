#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm

# rom djangobmf.layouts import Helper, Layout

from .models import Quotation


class QuotationUpdateForm(ModelForm):
    class Meta:
        model = Quotation
        exclude = ['quotation_number', ]


class QuotationCreateForm(ModelForm):
    class Meta:
        model = Quotation
        exclude = ['quotation_number', 'state', 'shipping_address', 'invoice_address', 'valid_until']
