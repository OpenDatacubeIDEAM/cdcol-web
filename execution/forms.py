# -*- coding: utf-8 -*-
from django import forms
from algorithm.models import Version


class VersionSelectionForm(forms.Form):
	version = forms.ModelChoiceField(queryset=None, widget=forms.Select())

	def __init__(self, *args, **kwargs):
		self.algorithm_id = kwargs.pop('algorithm_id')
		super(VersionSelectionForm, self).__init__(*args, **kwargs)
		self.fields['version'].queryset = Version.objects.filter(algorithm__id=self.algorithm_id)


class ReviewForm(forms.Form):
	rating = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'required': 'true', 'type': 'number', 'class': 'form-control'}))
	comments = forms.CharField(widget=forms.Textarea(attrs={'required': 'true', 'rows': 5, 'class': 'form-control',
	                                                        'placeholder': 'Ingresa detalles de la calidad de los resultados que obtuviste con la ejecución, la descripción del análisis realizaste, sobre qué región lo ejecutaste, etc.'}),
	                           required=True)
