#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from djangobmf.serializers import ModuleSerializer

from .models import Address


class AddressSerializer(ModuleSerializer):
    class Meta:
        model = Address
