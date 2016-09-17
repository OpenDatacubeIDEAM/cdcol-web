# -*- coding: utf-8 -*-
from django import forms
from algorithm.models import Topic
from storage.models import StorageUnit


class AlgorithmForm(forms.Form):
	topic = forms.ModelChoiceField(queryset=Topic.objects.all(), required=True)
	name = forms.CharField(max_length=200, required=True)
	description = forms.CharField(widget=forms.Textarea, required=True)
	source_storage_units = forms.ModelMultipleChoiceField(queryset=StorageUnit.objects.all(), required=True)


class AlgorithmUpdateForm(forms.Form):
	name = forms.CharField(max_length=200, required=True)
	description = forms.CharField(widget=forms.Textarea, required=True)
	source_storage_units = forms.ModelMultipleChoiceField(queryset=StorageUnit.objects.all(), required=True)


class VersionForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control',
								'placeholder': 'Ingresa una descripción de los cambios o ajustes realizados al algoritmo en esta nueva versión.'}),
	                            required=True)
	number = forms.CharField(max_length=200, required=True)
	source_code = forms.CharField(max_length=200, required=True)


class VersionUpdateForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control',
								'placeholder': 'Ingresa una descripción de los cambios o ajustes realizados al algoritmo en esta nueva versión.'}),
	                            required=True)
	source_code = forms.CharField(max_length=200, required=True)