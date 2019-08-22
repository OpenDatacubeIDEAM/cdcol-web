# -*- coding: utf-8 -*-

from django import forms
from storage.models import StorageUnit

class StorageUnitForm(forms.Form):
    """Storage unit creation form."""
    alias = forms.CharField(max_length=200, required=False)
    name = forms.CharField(max_length=200, required=False)
    description = forms.CharField(max_length=200, required=False)
    description_file = forms.FileField(required=True)
    ingest_file = forms.FileField(required=True)
    metadata_generation_script = forms.FileField(required=True)


class StorageUnitUpdateForm(forms.ModelForm):
    """Storage unit update form."""
    alias = forms.CharField(
    	label='Alias de la Unidad',
    	max_length=200, required=False,
    	help_text=''
    )
    name = forms.CharField(
    	label='Nombre de Unidad',
    	widget=forms.TextInput(
    		attrs={
    		'readonly':'readonly',
    		'placeholder': (
                    'Escriba el alias de la unidad de almacenamiento.' 
                )
    		}
    	)
    )

    class Meta:
        model = StorageUnit
        fields = ['alias','name']



