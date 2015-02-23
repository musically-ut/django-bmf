from .models import Document
from rest_framework import serializers


class ModuleSerializer(serializers.ModelSerializer):
    bmfdetail = serializers.SerializerMethodField()

    def get_bmfdetail(self, obj):
        return obj.bmfmodule_detail()


class DocumentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Document
        fields = ['pk']
