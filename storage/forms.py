from django import forms


class StorageUnitForm(forms.Form):
	alias = forms.CharField(max_length=200, required=False)
	name = forms.CharField(max_length=200, required=False)
	description = forms.CharField(max_length=200, required=False)
	description_file = forms.FileField(required=True)
	ingest_file = forms.FileField(required=True)
	metadata_generation_script = forms.FileField(required=True)

class StorageUnitUpdateForm(forms.Form):
	alias = forms.CharField(max_length=200, required=False)
