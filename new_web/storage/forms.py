# -*- coding: utf-8 -*-

from django import forms


class StorageUnitForm(forms.Form):
    """Storage unit creation form."""
    alias = forms.CharField(max_length=200, required=False)
    name = forms.CharField(max_length=200, required=False)
    description = forms.CharField(max_length=200, required=False)
    description_file = forms.FileField(required=True)
    ingest_file = forms.FileField(required=True)
    metadata_generation_script = forms.FileField(required=True)


class StorageUnitUpdateForm(forms.Form):
    """Storage unit update form."""
    alias = forms.CharField(max_length=200, required=False)
