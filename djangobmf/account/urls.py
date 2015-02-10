#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import LoginView
from .views import LogoutView
from .views import LogoutModal
from .views import PasswordChange

urlpatterns = patterns(
    '',
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^password/change/$', PasswordChange.as_view(), name="change_password"),
    url(r'^logout/modal/$', LogoutModal.as_view(), name="modal_logout"),
)
