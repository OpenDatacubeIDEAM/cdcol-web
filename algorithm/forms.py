from django import forms


class AlgorithmForm(forms.Form):
	topic = forms.CharField(max_length=200, required=True)
	name = forms.CharField(max_length=200, required=True)
	description = forms.CharField(widget=forms.Textarea, required=True)
	source_storage_units = forms.CharField(max_length=200, required=True)
	output_storage_unit = forms.CharField(max_length=200, required=True)
