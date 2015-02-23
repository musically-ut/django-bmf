#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.serializers import ModuleSerializer

from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(ModuleSerializer):
    test = serializers.SerializerMethodField()
    def test(self, obj):
        return 'asdasd'

    class Meta:
        model = Employee
