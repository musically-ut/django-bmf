#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django import forms
# from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.test import TestCase

from djangobmf.models import Configuration
from djangobmf.sites import site


class ModelTests(TestCase):
    def test_manager_get_settings_known_value(self):
        obj = Configuration(app_label='test', field_name='test1', value='"test1"')
        obj.save()
        site.register_settings("test", {
            'test1': forms.CharField(
                max_length=5,
            ),
        })
        with self.assertNumQueries(1):
            value = Configuration.get_setting('test', 'test1')
        self.assertEqual(value, "test1", "Load a known setting value from database")

        # test loading from cache
        with self.assertNumQueries(0):
            value = Configuration.get_setting('test', 'test1')

        self.assertEqual(value, "test1", "Load a known setting value from cache")

    def test_manager_get_settings_known_none(self):
        obj = Configuration(app_label='test', field_name='test5')
        obj.save()
        site.register_settings("test", {
            'test5': forms.CharField(
                max_length=5,
            ),
        })
        with self.assertNumQueries(1):
            value = Configuration.get_setting('test', 'test5')
        self.assertEqual(value, None, "Load a known setting value from database")

    def test_manager_get_settings_new_initial(self):
        site.register_settings("test", {
            'test2': forms.CharField(
                max_length=5,
                initial='test2',
            ),
        })
        value = Configuration.get_setting('test', 'test2')
        self.assertEqual(value, 'test2', "Load a new setting value from database")

    def test_manager_get_settings_new_none(self):
        site.register_settings("test", {
            'test3': forms.CharField(
                max_length=5,
            ),
        })
        value = Configuration.get_setting('test', 'test3')
        self.assertEqual(value, None, "Load a new setting value from database")

    def test_model_delete(self):
        obj = Configuration(app_label='test', field_name='test6')
        obj.save()
        obj.delete()

    def test_model_str(self):
        obj = Configuration(app_label='test', field_name='test7')
        obj.save()
        self.assertEqual('%s' % obj, 'test.test7', "Object string")

class ViewTests(TestCase):

    def test_list_view(self):
        """
        """
        pass
        # r = self.client.get(reverse('djangobmf:configuration'), {})
        # self.assertEqual(r.status_code, 302)

    def test_detail_view(self):
        """
        """
        pass
