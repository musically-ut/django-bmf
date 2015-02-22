from .models import Document
from rest_framework import serializers

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ['pk']
