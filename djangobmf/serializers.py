from .models import Document
from rest_framework import serializers


class ModuleSerializer(serializers.ModelSerializer):
    pass


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ['pk']
