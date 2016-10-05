# -*- coding: utf-8 -*-
from django import forms
from algorithm.models import Topic, Parameter
from storage.models import StorageUnit


class AlgorithmForm(forms.Form):
	topic = forms.ModelChoiceField(queryset=Topic.objects.all(), required=True)
	name = forms.CharField(max_length=200, required=True)
	description = forms.CharField(widget=forms.Textarea, required=True)


class AlgorithmUpdateForm(forms.Form):
	name = forms.CharField(max_length=200, required=True)
	description = forms.CharField(widget=forms.Textarea, required=True)


class VersionForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control',
								'placeholder': 'Ingresa una descripción de los cambios o ajustes realizados al algoritmo en esta nueva versión.'}),
	                            required=True)
	number = forms.CharField(max_length=200, required=True)
	source_code = forms.CharField(max_length=200, required=True)
	source_storage_units = forms.ModelMultipleChoiceField(queryset=StorageUnit.objects.all(), required=True)


class VersionUpdateForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control',
								'placeholder': 'Ingresa una descripción de los cambios o ajustes realizados al algoritmo en esta nueva versión.'}),
	                            required=True)
	source_code = forms.CharField(max_length=200, required=True)
	source_storage_units = forms.ModelMultipleChoiceField(queryset=StorageUnit.objects.all(), required=True)


class NewParameterForm(forms.Form):
	name = forms.CharField(max_length=200)
	parameter_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
	                                   choices=Parameter.PARAMETER_TYPES,
	                                   required=True)
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control',
	                              'placeholder': 'Ingresa una descripción del significado de este parámetro en la ejecución del algortimo.'}),
	                              required=True)
	help_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control',
	                              'placeholder': 'Ingresa un texto con las ayudas y consideraciones que deben tener en cuenta por los usuarios al ingresar este parámetro.'}),
	                              required=True)
	position = forms.IntegerField(min_value=0, required=True)
	required = forms.BooleanField(required=False)
	enabled = forms.BooleanField(required=False)
	default_value = forms.CharField(max_length=200, required=False)
	function_name = forms.CharField(max_length=200, required=True)

## TODO: Check this out https://spapas.github.io/2013/12/24/django-dynamic-forms/