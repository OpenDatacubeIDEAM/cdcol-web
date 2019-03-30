# -*- coding: utf-8 -*-

from django import forms

from algorithm.models import Version
from algorithm.models import Algorithm
from algorithm.models import Topic
from storage.models import StorageUnit


class AlgorithmCreateForm(forms.ModelForm):
    """Form to create algorithm."""

    class Meta:
        model = Algorithm
        fields = [
            'topic','name','description',
        ]

    topic = forms.ModelChoiceField(
        label='Temática',
        queryset=Topic.objects.filter(enabled=True),
        to_field_name='name',
    )
    name = forms.CharField(label='Nombre',max_length=200)
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


class AlgorithmUpdateForm(AlgorithmCreateForm):
    """Form to update algorithm."""

    class Meta:
        model = Algorithm
        fields = [
            'topic','name','description',
        ]

    topic = forms.ModelChoiceField(
        label='Temática',
        queryset=Topic.objects.filter(enabled=True),
        to_field_name="name",
        disabled=True,
    )


class ChoiceFieldNoValidation(forms.ChoiceField):
    """Field to avoid ChoiceField validation."""
    def validate(self, value):
        pass


class VersionCreateForm(forms.ModelForm):
    """Create version form."""

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
    number = ChoiceFieldNoValidation(label='Número de Versión')
    repository_url = forms.CharField(
        label='URL Código Fuente',max_length=200, required=True
    )
    source_storage_units = forms.ModelMultipleChoiceField(
        queryset=StorageUnit.objects.all(), required=True
    )


class VersionUpdateForm(forms.ModelForm):
    """Update version form."""

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
        label='Descripción de la Versión',
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
    number = forms.CharField(
        label='Número de la Versión',disabled=True
    )
    repository_url = forms.CharField(
        label='URL Código Fuente',max_length=200, required=True
    )
    source_storage_units = forms.ModelMultipleChoiceField(
        queryset=StorageUnit.objects.all(), required=True
    )