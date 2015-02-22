#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin


class ModuleListAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    """
    model = None
    module = None
    serializer = None
    permissions = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#   def post(self, request, *args, **kwargs):
#       return self.create(request, *args, **kwargs)


class ModuleDetailAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    """
    model = None
    module = None
    serializer = None
    permissions = None

#   def get(self, request, *args, **kwargs):
#       return self.retrieve(request, *args, **kwargs)

#   def put(self, request, *args, **kwargs):
#       return self.update(request, *args, **kwargs)

#   def patch(self, request, *args, **kwargs):
#       return self.partial_update(request, *args, **kwargs)

#   def delete(self, request, *args, **kwargs):
#       return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()
