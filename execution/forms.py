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
	REVIEW_TYPES = (
		(1, 1),
		(2, 2),
		(3, 3),
		(4, 4),
		(5, 5),
	)
	rating = forms.ChoiceField(
		widget=forms.Select(attrs={'required': 'true', 'class': 'form-control'}), choices=REVIEW_TYPES, required=True)
	comments = forms.CharField(widget=forms.Textarea(attrs={'required': 'true', 'rows': 5, 'class': 'form-control',
	                                                        'placeholder': 'Ingresa detalles de la calidad de los resultados que obtuviste con la ejecución, la descripción del análisis realizaste, sobre qué región lo ejecutaste, etc.'}),
	                           required=True)
