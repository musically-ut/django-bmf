#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.serializers import ModuleSerializer

from rest_framework import serializers

from .models import Project


class ProjectSerializer(ModuleSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.name')

    class Meta:
        model = Project
        fields = (
            'name',
            'is_active',
            'customer',
            'customer_name',
            'bmfdetail',
        )
