#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.http import Http404

from rest_framework.permissions import BasePermission


class ModulePermission(BasePermission):
    """
    Permission object to check the module's permissions
    """

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.view_%(model_name)s', '%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        model_cls = getattr(view, 'model', None)
        perms = self.get_permissions(request.method, model_cls)
        return request.user.has_perms(perms)

    def has_object_permission(self, request, view, obj):
        model_cls = getattr(view, 'model', None)
        perms = self.get_permissions(request.method, model_cls)

        if not request.user.has_perms(perms, obj):
            # If the user does not have permissions we need to determine if
            # they have read permissions to see 403, or not, and simply see
            # a 404 response.

            if request.method in ['GET', 'OPTIONS', 'HEAD']:
                # Read permissions already checked and failed, no need
                # to make another lookup.
                raise Http404

            read_perms = self.get_permissions('GET', model_cls)
            if not request.user.has_perms(read_perms, obj):
                raise Http404

            # Has read permissions - generate 403 response
            return False

        # Has permissions to view object
        return True

    def filter_queryset(self, qs, user, model_cls):
        return qs

    def get_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            'app_label': model_cls._meta.app_label,
            'model_name': model_cls._meta.model_name,
        }
        return [perm % kwargs for perm in self.perms_map[method]]
