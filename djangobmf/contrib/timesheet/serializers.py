#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.formats import date_format
from django.utils.timezone import now

from djangobmf.serializiers import ModuleSerializer

from rest_framework import serializers

from .models import Timesheet


class TimesheetSerializer(ModuleSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Timesheet

    def date(self, obj):
        return date_format(obj.start, "SHORT_DATE_FORMAT"),

    def time(self, obj):
        if obj.end:
            return obj.end - obj.start,
        else:
            return now() - obj.start,
