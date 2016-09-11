from django import forms
from algorithm.models import Topic
from storage.models import StorageUnit


class AlgorithmForm(forms.Form):
	topic = forms.ModelChoiceField(queryset=Topic.objects.all(), required=True)
	name = forms.CharField(max_length=200, required=True)
	description = forms.CharField(widget=forms.Textarea, required=True)
	source_storage_units = forms.ModelMultipleChoiceField(queryset=StorageUnit.objects.all(), required=True)
	output_storage_unit = forms.CharField(max_length=200, required=True)
