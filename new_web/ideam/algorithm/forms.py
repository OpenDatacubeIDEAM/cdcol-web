# -*- coding: utf-8 -*-

from django import forms

from algorithm.models import Version
from algorithm.models import Algorithm
from storage.models import StorageUnit


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass

class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = [ 
            'algorithm','number','description',
            'repository_url','source_storage_units'
        ]

    algorithm = forms.ModelChoiceField(
        label='Algoritmo',
        queryset=Algorithm.objects.all(),
        to_field_name="name",
        widget=forms.TextInput(attrs={'readonly':'readonly'}),
    )
    description = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(
                attrs={
                'rows': 5, 
                'class': 'form-control', 
                'required': 'True',
                'placeholder': (
                    'Ingrese una descripción de los cambios o ajustes ' 
                    'realizados al algoritmo en esta nueva versión.'
                )
            }
        )
    )
    number = ChoiceFieldNoValidation(
        label='Número de Nueva Versión',
        
        # required=True
    )
    repository_url = forms.CharField(max_length=200, required=True)
    source_storage_units = forms.ModelMultipleChoiceField(
        queryset=StorageUnit.objects.all(), required=True
    )


