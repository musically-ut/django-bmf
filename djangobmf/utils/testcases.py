#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase as DjangoLiveServerTestCase
from django.test import TransactionTestCase as DjangoTransactionTestCase
from django.test import TestCase as DjangoTestCase
from django.utils.translation import activate

from djangobmf.demo import FIXTURES
from djangobmf.settings import APP_LABEL
from djangobmf.settings import CONTRIB_EMPLOYEE
from djangobmf.sites import site

from collections import OrderedDict

import json

# from unittest import expectedFailure


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


class DemoDataMixin(object):
    """
    Adds the demo data from the fixtures to the testcase
    """
    fixtures = FIXTURES


class SuperuserMixin(object):
    """
    Adds a superuser to the clients and authenticates itself with this user
    """

    def setUp(self):  # noqa
        super(SuperuserMixin, self).setUp()
        self.user = self.create_user("superuser", is_superuser=True)
        self.client_login("superuser")


class ModuleTestFactory(SuperuserMixin, BaseTestCase):
    """
    Test generic module views within app-config ``app``

    Currently detail, get and list views are tested.

    The test includes only the template rendering of those classes. No
    data is accessed or changed.
    """

    # the modules app config
    app = None

    def setUp(self):  # noqa
        super(BaseTestCase, self).setUp()
        self.user = self.create_user("superuser", is_superuser=True)
        self.client_login("superuser")
        self.appconf = [app for app in apps.get_app_configs() if isinstance(app, self.app)][0]
        self.models = [m for m in self.appconf.get_models() if m in site.models.values()]

    def test_module_create(self):
        for model in self.models:

            ns = model._bmfmeta.namespace_api

            for key, slug, view in site.modules[model].list_creates():
                url = reverse('%s:create' % ns, kwargs={
                    'key': key,
                })
                response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
                self.assertEqual(response.status_code, 200)

    def test_module_update(self):
        for model in self.models:
            ns = model._bmfmeta.namespace_api

            for obj in model.objects.all():
                url = reverse('%s:update' % ns, kwargs={
                    'pk': obj.pk,
                })
                response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
                self.assertTrue(response.status_code in [200, 403])

    def test_module_delete(self):
        for model in self.models:
            ns = model._bmfmeta.namespace_api

            for obj in model.objects.all():
                url = reverse('%s:delete' % ns, kwargs={
                    'pk': obj.pk,
                })
                response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
                self.assertTrue(response.status_code in [200, 403])

    def test_module_detail(self):
        for model in self.models:
            for obj in model.objects.all():
                response = self.client.get(obj.bmfmodule_detail())
                self.assertEqual(response.status_code, 200)

    def test_module_lists_and_gets(self):
        views = []
        for model in self.models:
            for dashboard in site.dashboards:
                for category in dashboard:
                    for view in category:
                        if view.model == model:
                            views.append((model, view, dashboard.key, category.key, view.key))

        for v in views:
            url = reverse('%s:dashboard_view' % APP_LABEL, kwargs={
                'dashboard': v[2],
                'category': v[3],
                'view': v[4],
            })
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

            url = response.context['get_data_url']

            response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200)

    def prepare_workflow_test(self, workflow_cls):
        workflow = workflow_cls()

        states = list(workflow._states.keys())
        states.remove(workflow._initial_state_key)
        heap = [
            (workflow._initial_state_key + '->' + key + '->' + transition.target)
            for key, transition in workflow._from_here()
        ]

        heap.reverse()
        objects = {workflow._initial_state_key: None}
        transitions = OrderedDict()

        while len(heap) > 0:
            current = heap.pop()
            obj, transition, target = current.split('->')
            transitions[current] = {
                'object': None,
                'object_key': obj,
                'state': obj.rsplit(':', 1)[-1],
                'user': None,
                'transition': transition,
            }

            if target in states:
                workflow._set_state(target)
                objects['%s:%s' % (obj, target)] = None
                for key, transition in workflow._from_here():
                    heap.insert(0, '%s:%s->%s->%s' % (
                        obj,
                        target,
                        key,
                        transition.target,
                    ))
                states.remove(target)

        return transitions, objects

    def auto_workflow_test(self, transitions, objects):
        for key, trans in transitions.items():

            obj = trans['object'] or objects.get(trans['object_key'])

            if not obj:
                raise ImproperlyConfigured(
                    'No object given for transitions["%s"]' % key
                )

            if obj._bmfmeta.workflow.key != trans['state']:
                raise ImproperlyConfigured(
                    'Object "%s" is in the wrong state for transitions["%s"]' % (
                        obj,
                        key,
                    )
                )

            user = trans['user'] or self.user

            # this does not work, we need to copy the object instance
            # otherwise the stored object is changed and the next loop fails

            if not obj.pk:
                obj.save()

            oldpk = obj.pk
            obj.pk = None
            obj.save()
            newpk = obj.pk
            obj.pk = oldpk

            new_obj = obj.__class__.objects.get(pk=newpk)

            # use collector to copy related objects
            # from django.contrib.admin.utils import NestedObjects
            # collector = NestedObjects(using='default')
            # collector.collect([obj])
            # print(collector.nested())

            # print('')
            # print(obj.state, new_obj.pk)
            # print(new_obj.state, new_obj.pk)
            # print(trans['transition'])
            new_obj._bmfmeta.workflow.transition(trans['transition'], user)
            # print(new_obj.state, new_obj.pk)

            if trans['object_key']:
                new_key = '%s:%s' % (
                    trans['object_key'],
                    new_obj._bmfmeta.workflow.key
                )

                if not objects.get(new_key, None):
                    objects[new_key] = new_obj


class ModuleMixin(SuperuserMixin):
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
