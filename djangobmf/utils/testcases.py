#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase as DjangoLiveServerTestCase
from django.test import TransactionTestCase as DjangoTransactionTestCase
from django.test import TestCase as DjangoTestCase
from django.utils.translation import activate

from djangobmf.settings import CONTRIB_EMPLOYEE
from djangobmf.sites import site

import json


class BaseTestCase(object):
    def setUp(self):  # noqa
        site.activate(test=True)
        activate('en')

        super(BaseTestCase, self).setUp()

    def create_user(self, username, is_staff=False, is_superuser=False,
                    is_active=True, permissions=None, create_employee=True):
        """
        This method is used to create users in test cases
        """
        user = get_user_model()
        username_field = user.USERNAME_FIELD

        fields = {
            'email': username + '@test.django-bmf.org',
            'is_staff': is_staff,
            'is_active': is_active,
            'is_superuser': is_superuser,
        }

        # Check for special case where email is used as username
        # if username_field != 'email':
        fields[username_field] = username

        user_obj = user(**fields)
        user_obj.set_password(getattr(user_obj, username_field))
        user_obj.save()

        # create employee object for user
        try:
            apps.get_model(CONTRIB_EMPLOYEE).objects.create(user=user_obj)
        except LookupError:
            pass

        if not is_superuser and permissions:
            for permission in permissions:
                user_obj.user_permissions.add(Permission.objects.get(codename=permission))

        return user_obj

    def client_login(self, username):
        # Check for special case where email is used as username
        # if get_user_model().USERNAME_FIELD == 'email':
        #     username += '@test.django-bmf.org'

        # update client
        self.client.login(username=username, password=username)


class ModuleMixin(object):
    model = None

    def get_latest_object(self):
        return self.model.objects.order_by('pk').last()

    def autotest_get(
            self, namespace=None, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None, url=None, api=True):
        """
        tests the POST request of a view, returns the response
        """
        if api:
            ns = self.model._bmfmeta.namespace_api
        else:
            ns = self.model._bmfmeta.namespace_detail
        if not url:
            url = reverse(ns + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.get(url, data)
        self.assertEqual(r.status_code, status_code)
        return r

    def autotest_post(
            self, namespace=None, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None, url=None, api=True):
        """
        tests the GET request of a view, returns the response
        """
        if api:
            ns = self.model._bmfmeta.namespace_api
        else:
            ns = self.model._bmfmeta.namespace_detail
        if not url:
            url = reverse(ns + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status_code)
        return r

    def autotest_ajax_get(
            self, namespace=None, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None, url=None, api=True):
        """
        tests the GET request of an ajax-view, returns the serialized data
        """
        if api:
            ns = self.model._bmfmeta.namespace_api
        else:
            ns = self.model._bmfmeta.namespace_detail
        if not url:
            url = reverse(ns + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.get(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, status_code)
        if status_code == 200:
            return json.loads(r.content.decode())
        return r

    def autotest_ajax_post(
            self, namespace=None, status_code=200, data=None, parameter=None,
            urlconf=None, args=None, kwargs=None, current_app=None, url=None, api=True):
        """
        tests the POST request of an ajax-view, returns the serialized data
        """
        if api:
            ns = self.model._bmfmeta.namespace_api
        else:
            ns = self.model._bmfmeta.namespace_detail
        if not url:
            url = reverse(ns + ':' + namespace, urlconf, args, kwargs, current_app)
        if parameter:
            url += '?' + parameter
        r = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, status_code)
        if status_code == 200:
            return json.loads(r.content.decode())
        return r


class TestCase(BaseTestCase, DjangoTestCase):
    pass


class TransactionTestCase(BaseTestCase, DjangoTransactionTestCase):
    pass


class LiveServerTestCase(BaseTestCase, DjangoLiveServerTestCase):
    pass
