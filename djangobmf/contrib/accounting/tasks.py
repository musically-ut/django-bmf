#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db.models import Sum

from djangobmf.settings import USE_CELERY
from djangobmf.settings import CONTRIB_ACCOUNT
from djangobmf.settings import CONTRIB_TRANSACTIONITEM
from djangobmf.utils.model_from_name import model_from_name

from decimal import Decimal

import logging
logger = logging.getLogger(__name__)


# business logic


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
        bmfcontrib_accounting_calc_balance(model.pk)


# make celery optional


if USE_CELERY:
    from celery import shared_task

    @shared_task
    def djangobmf_contrib_accounting_calc_balance(*args):
        return _calc_account_balance(*args)
else:
    def djangobmf_contrib_accounting_calc_balance(*args):
        return _calc_account_balance(*args)


# call this functions


def bmfcontrib_accounting_calc_balance(*args):

    if USE_CELERY:
        return djangobmf_contrib_accounting_calc_balance.apply_async(args)
    logger.debug("Running task bmfcontrib_accounting_calc_balance without celery")
    return djangobmf_contrib_accounting_calc_balance(*args)
