#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.categories import BaseCategory
from djangobmf.categories import ViewFactory
from djangobmf.categories import Accounting
from djangobmf.sites import site

# from .models import ACCOUNTING_INCOME
# from .models import ACCOUNTING_EXPENSE
# from .models import ACCOUNTING_ASSET
# from .models import ACCOUNTING_LIABILITY
from .models import Account
from .models import Transaction
from .models import TransactionItem

from .views import TransactionCreateView
from .views import TransactionUpdateView


site.register_module(Account)


site.register_module(Transaction, **{
    'create': TransactionCreateView,
    'update': TransactionUpdateView,
})


site.register_module(TransactionItem)


# SETTINGS = {
#     'income': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_INCOME)),
#     'expense': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_EXPENSE)),
#     'customer': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_ASSET)),
#     'supplier': forms.ModelChoiceField(queryset=Account.objects.filter(type=ACCOUNTING_LIABILITY)),
# }
# site.register_settings(AccountingConfig.label, SETTINGS)


class TransactionCategory(BaseCategory):
    name = _('Transactions')
    slug = "transactions"


site.register_dashboards(
    Accounting(
        TransactionCategory(
            ViewFactory(
                model=Account,
                name=_("All Accounts"),
                slug="accounts",
            ),
            ViewFactory(
                model=Transaction,
                name=_("Open transactions"),
                slug="open",
                manager="open",
            ),
            ViewFactory(
                model=Transaction,
                name=_("Closed transactions"),
                slug="closed",
                manager="closed",
                date_resolution="month",
            ),
            ViewFactory(
                model=TransactionItem,
                name=_("Transaction archive"),
                slug="archive",
                date_resolution="week",
            ),
        ),
    ),
)
