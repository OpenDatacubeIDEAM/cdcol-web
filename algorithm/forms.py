# -*- coding: utf-8 -*-
from django import forms
from algorithm.models import Topic, Parameter
from storage.models import StorageUnit


class AlgorithmForm(forms.Form):
	topic = forms.ModelChoiceField(queryset=Topic.objects.filter(enabled=True), required=True)
	name = forms.CharField(max_length=200, required=True)
	description = forms.CharField(widget=forms.Textarea, required=True)


class AlgorithmUpdateForm(forms.Form):
	name = forms.CharField(max_length=200, required=True)
	description = forms.CharField(widget=forms.Textarea, required=True)


class VersionForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'required': 'True',
								'placeholder': 'Ingrese una descripción de los cambios o ajustes realizados al algoritmo en esta nueva versión.'}))
	number = forms.CharField(max_length=200, required=True)
	repository_url = forms.CharField(max_length=200, required=True)
	source_storage_units = forms.ModelMultipleChoiceField(queryset=StorageUnit.objects.all(), required=True)


class VersionUpdateForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'required': 'True',
								'placeholder': 'Ingrese una descripción de los cambios o ajustes realizados al algoritmo en esta nueva versión.'}))
	repository_url = forms.CharField(max_length=200, required=True)
	source_storage_units = forms.ModelMultipleChoiceField(queryset=StorageUnit.objects.all(), required=True)


class NewParameterForm(forms.Form):
	name = forms.CharField(max_length=200)
	parameter_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
	                                   choices=Parameter.PARAMETER_TYPES,
	                                   required=True)
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'required': 'True',
	                              'placeholder': 'Ingrese una descripción del significado de este parámetro en la ejecución de la versión algortimo.'}))
	help_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control',
	                              'placeholder': 'Ingrese un texto con las ayudas y consideraciones que deben ser tenidas en cuenta por los usuarios al ingresar este parámetro.'}),
	                              required=True)
	position = forms.IntegerField(min_value=0, required=True)
	required = forms.BooleanField(required=False, initial=True)
	enabled = forms.BooleanField(required=False, initial=True)
	default_value = forms.CharField(max_length=200, required=False)
	function_name = forms.CharField(max_length=200, required=True)
	output_included = forms.BooleanField(required=False, initial=True)
