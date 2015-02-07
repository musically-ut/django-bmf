#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import TestCase

from djangobmf.views.mixins import BaseMixin
from djangobmf.views.mixins import ViewMixin
from djangobmf.views.mixins import AjaxMixin
from djangobmf.views.mixins import ModuleViewPermissionMixin
from djangobmf.views.mixins import ModuleCreatePermissionMixin
from djangobmf.views.mixins import ModuleUpdatePermissionMixin
from djangobmf.views.mixins import ModuleDeletePermissionMixin
from djangobmf.views.mixins import ModuleClonePermissionMixin

from djangobmf.views.mixins import ModuleBaseMixin
from djangobmf.views.mixins import ModuleAjaxMixin

from unittest import expectedFailure

from .models import TestView

class MixinTests(TestCase):

    def test_basemixin_get_permissions1(self):
        obj = BaseMixin()
        obj.model = TestView
        self.assertEqual(obj.get_permissions(), [])
        self.assertEqual(obj.get_permissions(['test']), ['test'])

    def test_basemixin_get_permissions2(self):
        obj = BaseMixin()
        obj.model = TestView
        obj.permissions = ['test2']
        self.assertEqual(obj.get_permissions(), ['test2'])
        self.assertEqual(obj.get_permissions(['test']), ['test','test2'])

    def test_basemixin_check_permissions(self):
        obj = BaseMixin()
        obj.model = TestView
        self.assertEqual(obj.check_permissions(), True)

    @expectedFailure
    def test_basemixin_read_session_data(self):
        obj = BaseMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_basemixin_write_session_data(self):
        obj = BaseMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_basemixin_dispatch(self):
        obj = BaseMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_basemixin_update_workspace(self):
        obj = BaseMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_basemixin_update_notification(self):
        obj = BaseMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_viewmixin_get_context_data(self):
        obj = ViewMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_ajaxmixin_dispatch(self):
        obj = AjaxMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_ajaxmixin_check_permisions(self):
        obj = AjaxMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_ajaxmixin_render_to_json_response(self):
        obj = AjaxMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_ajaxmixin_get_ajax_context(self):
        obj = AjaxMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_ajaxmixin_render_to_response(self):
        obj = AjaxMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_ajaxmixin_render_valid_form(self):
        obj = AjaxMixin()
        obj.model = TestView
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    def test_moduleviewpermissionmixin(self):
        class Test(ModuleViewPermissionMixin, BaseMixin):
            model = None
        obj = Test()
        obj.model = TestView
        self.assertEqual(obj.get_permissions(), ['appapis.view_testview'])

    def test_modulecreatepermissionmixin(self):
        class Test(ModuleCreatePermissionMixin, BaseMixin):
            model = None
        obj = Test()
        obj.model = TestView
        self.assertEqual(sorted(obj.get_permissions()), ['appapis.add_testview','appapis.view_testview'])

    def test_moduleclonepermissionmixin(self):
        class Test(ModuleClonePermissionMixin, BaseMixin):
            model = None
        obj = Test()
        obj.model = TestView
        self.assertEqual(sorted(obj.get_permissions()), ['appapis.clone_testview','appapis.view_testview'])

    def test_moduleupdatepermissionmixin1(self):
        class Test(ModuleUpdatePermissionMixin, BaseMixin):
            model = None
        obj = Test()
        obj.model = TestView
        self.assertEqual(sorted(obj.get_permissions()), ['appapis.change_testview','appapis.view_testview'])

#   TODO: This test fails on travis, but can not reproduced in local
#   def test_moduleupdatepermissionmixin2(self):
#       class Test(ModuleUpdatePermissionMixin, BaseMixin):
#           model = TestView
#           def get_object(self):
#               return TestView()
#       obj = Test()
#       self.assertFalse(obj.check_permissions())

    def test_moduledeletepermissionmixin1(self):
        class Test(ModuleDeletePermissionMixin, BaseMixin):
            model = None
        obj = Test()
        obj.model = TestView
        self.assertEqual(sorted(obj.get_permissions()), ['appapis.delete_testview','appapis.view_testview'])

#   TODO: This test fails on travis, but can not reproduced in local
#   def test_moduledeletepermissionmixin2(self):
#       class Test(ModuleDeletePermissionMixin, BaseMixin):
#           model = TestView
#           def get_object(self):
#               return TestView()
#       obj = Test()
#       self.assertFalse(obj.check_permissions())

    @expectedFailure
    def test_modulebasemixin_get_queryset(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_modulebasemixin_get_object(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_modulebasemixin_get_context_data(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_moduleajaxmixin_get_ajax_data(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED

    @expectedFailure
    def test_moduleajaxmixin_render_valid_form(self):
        self.assertTrue(False)  # TODO NOT IMPLEMENTED
