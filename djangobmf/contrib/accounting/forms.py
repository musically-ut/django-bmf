#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm
from django.forms import ModelChoiceField
from django.forms import FloatField
from django.forms import BooleanField
from django.utils.translation import ugettext_lazy as _

from djangobmf.settings import CONTRIB_ACCOUNT
from djangobmf.utils.model_from_name import model_from_name
# from djangobmf.fields import CurrencyField
# from djangobmf.fields import MoneyField

from .models import Transaction
# from .models import TransactionItem


account = model_from_name(CONTRIB_ACCOUNT)


class TransactionUpdateForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = []


class TransactionCreateForm(ModelForm):

    debit = ModelChoiceField(queryset=account.objects.filter(read_only=False), empty_label=None)
    credit = ModelChoiceField(queryset=account.objects.filter(read_only=False), empty_label=None)
    # amount_currency = CurrencyField()
    # amount = MoneyField()
    amount = FloatField(label=_("Amount"), min_value=0, localize=True)
    draft = BooleanField(label=_("Create draft"), initial=True, required=False)

    class Meta:
        model = Transaction
        exclude = []
