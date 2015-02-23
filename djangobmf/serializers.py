from .models import Document
from rest_framework import serializers


class ModuleSerializer(serializers.ModelSerializer):
    bmfmodule_detail = serializers.SerializerMethodField()

    def get_bmfmodule_detail(self, obj):
        return obj.bmfmodule_detail()


class DocumentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Document
        fields = ['pk']
