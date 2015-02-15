#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from .apps import AccountingConfig
from .models import Account

from djangobmf.utils.testcases import TestCase
from djangobmf.utils.testcases import ModuleMixin
from djangobmf.utils.testcases import DemoDataMixin
from djangobmf.utils.testcases import ModuleTestFactory


class AccountingFactory(ModuleTestFactory, DemoDataMixin, TestCase):
    app = AccountingConfig


class AccountModuleTests(ModuleMixin, TestCase):
    pass

#   # this test fails because the currency is set to none
#   def test_get_urls(self):
#       """
#       """
#       self.model = Account

#       data = self.autotest_ajax_post('create', kwargs={'key': 'default'}, data={
#           'number': "1",
#           'name': "account 1",
#           'type': 50,
#       })

#       obj = self.get_latest_object()
#       a = '%s'%obj # check if object name has any errors

#       data = self.autotest_ajax_get('update', kwargs={'pk': obj.pk})
#       self.autotest_ajax_post('delete', kwargs={'pk': obj.pk})
