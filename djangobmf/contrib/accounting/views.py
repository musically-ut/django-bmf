#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleArchiveView
from djangobmf.views import ModuleListView
# from djangobmf.views import ModuleTreeView
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
# from djangobmf.views import ModuleDetailView

# from .models import Account

from .forms import TransactionUpdateForm
from .forms import TransactionCreateSimpleForm
from .forms import TransactionCreateSplitForm


class AccountIndexView(ModuleListView):
    name = _("All Accounts")
    slug = "accounts"


class AllTransactionView(ModuleArchiveView):
    name = _("All Transactions")
    slug = "transactions"
    date_resolution = "month"


class ClosedTransactionView(ModuleArchiveView):
    name = _("Closed Transactions")
    slug = "closed"
    date_resolution = "week"

    def get_queryset(self):
        return super(ClosedTransactionView, self).get_queryset().filter(draft=False).order_by('-modified')


class OpenTransactionView(ModuleListView):
    name = _("Open Transactions")
    slug = "items"

    def get_queryset(self):
        return super(OpenTransactionView, self).get_queryset().filter(draft=True).order_by('modified')


class TransactionCreateSimpleView(ModuleCreateView):
    form_class = TransactionCreateSimpleForm

    def form_object_save(self, form):
        super(TransactionCreateSimpleView, self).form_object_save(form)

        self.object.items.create(
            account=form.cleaned_data['debit'],
            credit=False,
            amount=form.cleaned_data['amount'],
        )
        self.object.items.create(
            account=form.cleaned_data['credit'],
            credit=True,
            amount=form.cleaned_data['amount'],
        )

        if form.cleaned_data['execute'] is True:
            self.object.bmfworkflow_transition('balance', self.request.user)


class TransactionCreateSplitView(ModuleCreateView):
    form_class = TransactionCreateSplitForm


class TransactionUpdateView(ModuleUpdateView):
    form_class = TransactionUpdateForm
