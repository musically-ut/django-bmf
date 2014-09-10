#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.views.generic import TemplateView

from ..views import BaseMixin

class MessageView(BaseMixin, TemplateView):
    template_name = "djangoerp/message/index.html"

