from django import forms


class CDCOLForm(forms.Form):
	processing_level = forms.CharField(max_length=200, required=True)
	detailed_processing_level = forms.CharField(max_length=200, required=True)
	file = forms.FileField(required=True)
