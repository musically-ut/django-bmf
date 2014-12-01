#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import TestCase
from djangobmf.sites import autodiscover

from unittest import expectedFailure


class AutodiscoverTests(TestCase):
    @expectedFailure
    def test_fails(self):
        self.assertTrue(False)
