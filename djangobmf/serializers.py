from .models import Document
# from .fields import WorkflowField
from rest_framework import serializers


class ModuleSerializer(serializers.ModelSerializer):
    bmfdetail = serializers.SerializerMethodField()

    def get_bmfdetail(self, obj):
        return obj.bmfmodule_detail()


# ModuleSerializer._field_mapping[WorkflowField] = WorkflowField


class DocumentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Document
        fields = ['pk']
