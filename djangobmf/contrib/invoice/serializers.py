#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.serializers import ModuleSerializer

from rest_framework import serializers

from .models import Invoice


class InvoiceSerializer(ModuleSerializer):
    state_name = serializers.ReadOnlyField(source='state.name')
    project_name = serializers.ReadOnlyField(source='project.name')

    class Meta:
        model = Invoice
        fields = (
            'invoice_number',
            'state',
            'state_name',
            'project',
            'project_name',
            'bmfdetail',
        )
