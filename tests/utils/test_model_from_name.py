#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from djangobmf.utils.model_from_name import model_from_name


class ModelFromNameTests(TestCase):
    def test_valid_model(self):
        out = model_from_name("contenttypes.ContentType")
        self.assertEqual(out, ContentType)

    def test_invalid_model(self):
        out = model_from_name("does_not.Exist")
        self.assertEqual(out, None)
