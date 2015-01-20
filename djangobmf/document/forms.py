from django import forms

from djangobmf.models import Document


class UploadDocument(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['file']
