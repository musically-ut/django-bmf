#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.serializers import ModuleSerializer

from .models import Account
from .models import Transaction
from .models import TransactionItem


class AccountSerializer(ModuleSerializer):

    class Meta:
        model = Account


class TransactionSerializer(ModuleSerializer):

    class Meta:
        model = Transaction


class TransactionItemSerializer(ModuleSerializer):

    class Meta:
        model = TransactionItem
