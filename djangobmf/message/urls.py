#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.conf.urls import patterns, url

from .views import MessageView

urlpatterns = patterns('',
    url(r'^$', MessageView.as_view(), name="message"),
)
