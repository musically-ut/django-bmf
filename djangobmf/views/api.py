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

    def get_queryset(self):
        print("GET QUERYSET")
        return self.model.objects.all()

    def get_serializer_class(self):
        print("GET SERIALIZER")
        return self.serializer


class ModuleDetailAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    """
    model = None
    module = None
    serializer_class = None

    def get_queryset(self):
        return self.model.objects.all()
