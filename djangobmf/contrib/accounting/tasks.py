#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db.models import Sum

from djangobmf.decorators import optional_celery
from djangobmf.settings import CONTRIB_ACCOUNT
from djangobmf.settings import CONTRIB_TRANSACTIONITEM
from djangobmf.utils.model_from_name import model_from_name

from decimal import Decimal

import logging
logger = logging.getLogger(__name__)


def _calc_account_balance(pk):
    account_mdl = model_from_name(CONTRIB_ACCOUNT)
    transaction_mdl = model_from_name(CONTRIB_TRANSACTIONITEM)
    account = account_mdl.objects.get(pk=pk)
    pks = list(account.get_descendants(include_self=True).values_list('pk', flat=True))

    credit = transaction_mdl.objects.filter(
        account_id__in=pks,
        draft=False,
        credit=True,
    ).aggregate(Sum('amount'))

    debit = transaction_mdl.objects.filter(
        account_id__in=pks,
        draft=False,
        credit=False,
    ).aggregate(Sum('amount'))

    value_credit = credit['amount__sum'] or Decimal(0)
    value_debit = debit['amount__sum'] or Decimal(0)

    if account.credit_increase():
        account.balance = value_debit - value_credit
    else:
        account.balance = value_credit - value_debit

    account.save()

    for model in account.get_ancestors():
        _calc_account_balance(model.pk)


@optional_celery
def calc_account_balance(pk):
    _calc_account_balance(pk)
