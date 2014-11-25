#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.db.models import Sum

from djangobmf.settings import USE_CELERY
from djangobmf.settings import CONTRIB_ACCOUNT
from djangobmf.utils.model_from_name import model_from_name

from decimal import Decimal


# business logic


def _calc_account_balance(pk):
    account_mdl = model_from_name(CONTRIB_ACCOUNT)
    account = account_mdl.objects.get(pk=pk)

    credit = account.transactions.filter(
        draft=False,
        credit=True,
    ).aggregate(Sum('amount'))

    debit = account.transactions.filter(
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
    return djangobmf_contrib_accounting_calc_balance(*args)
