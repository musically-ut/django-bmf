#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.utils.user import user_add_bmf

from rest_framework import pagination
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin


class PaginationSerializer(serializers.Serializer):
    next = pagination.NextPageField(source='*')
    prev = pagination.PreviousPageField(source='*')
    total_results = serializers.ReadOnlyField(source='paginator.count')


class ModulePaginationSerializer(pagination.BasePaginationSerializer):
    # Takes the page object as the source
    pagination = PaginationSerializer(source='*')
    results_field = 'items'


class ModuleListAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    """
    model = None
    module = None
    permissions = None
    pagination_serializer_class = ModulePaginationSerializer
    paginate_by = 100

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#   def post(self, request, *args, **kwargs):
#       return self.create(request, *args, **kwargs)

    def get_queryset(self):
        manager = self.kwargs.get('manager', 'all')
        if manager == 'all':
            qs = self.model.objects.all()
        else:
            # TODO
            qs = self.model.objects.all()

        user_add_bmf(self.request.user)

        return self.permissions().filter_queryset(
            qs,
            self.request.user,
            self.model
        )

    def get_permissions(self):
        perms = super(ModuleListAPIView, self).get_permissions()
        return [self.permissions()] + perms


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
