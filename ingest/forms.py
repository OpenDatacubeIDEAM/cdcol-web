# -*- coding: utf-8 -*-
from django import forms
from storage.models import StorageUnit


class IngestTaskForm(forms.Form):
	storage_unit = forms.ModelChoiceField(queryset=StorageUnit.objects.all(), required=True)
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control',
								'placeholder': 'Ingrese una descripción que le ayude a identificar la tarea de ingesta que se va a ejecutar sobre la unidad de almacenamiento'}),
	                            required=True)
