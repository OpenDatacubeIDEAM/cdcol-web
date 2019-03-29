# -*- coding: utf-8 -*-

from django import forms

from algorithm.models import Version
from storage.models import StorageUnit


class VersionForm(forms.ModelForm):

    description = forms.CharField(
        widget=forms.Textarea(
                attrs={
                'rows': 5, 
                'class': 'form-control', 
                'required': 'True',
                'placeholder': (
                    'Ingrese una descripción de los cambios o ajustes ' 
                    'realizados al algoritmo en esta nueva versión.'
                )
            }
        )
    )
    number = forms.CharField(max_length=200, required=True)
    repository_url = forms.CharField(max_length=200, required=True)
    source_storage_units = forms.ModelMultipleChoiceField(
        queryset=StorageUnit.objects.all(), required=True
    )

    class Meta:
        model = Version
        fields = [ 'algorithm','number','description','repository_url','source_storage_units']
