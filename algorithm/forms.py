# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from algorithm.models import Version
from algorithm.models import Algorithm
from algorithm.models import Topic
from algorithm.models import Parameter
from storage.models import StorageUnit

import os


class AlgorithmCreateForm(forms.ModelForm):
    """Form to create algorithm."""

    class Meta:
        model = Algorithm
        fields = [
            'topic','name','description',
        ]

    topic = forms.ModelChoiceField(
        label='Temática',
        queryset=Topic.objects.filter(enabled=True)
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
        queryset=Topic.objects.filter(enabled=True)
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
            'show_algorthm_name',
            'algorithm',
            'name',
            'number',
            'description',
            'repository_url',
            # 'source_storage_units'
        ]

    # This field only show the algorithm name to be related with the 
    # version to the user
    show_algorthm_name = forms.CharField(
        label='Algoritmo',
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    # This fied is hidden so that the user can not modify 
    # its value
    algorithm = forms.ModelChoiceField(
        label='Algoritmo',
        queryset=Algorithm.objects.all(),
        widget=forms.HiddenInput(),
    )

    name = forms.CharField(label='Nombre de la Version',max_length=200)

    number = ChoiceFieldNoValidation(label='Número de Versión')

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
    
    repository_url = forms.CharField(
        label='URL Código Fuente',max_length=200, required=True
    )
    
    source_storage_units = forms.ModelMultipleChoiceField(
        label='Posibles unidades de almacenamiento origen',
        queryset=StorageUnit.objects.all(), required=True
    )


class VersionUpdateForm(forms.ModelForm):
    """Update version form."""

    class Meta:
        model = Version
        fields = [
            'show_algorthm_name',
            'algorithm',
            'name',
            'number',
            'description',
            'repository_url',
            # 'source_storage_units'
        ]

    # This field only show the algorithm name to be related with the 
    # version to the user
    show_algorthm_name = forms.CharField(
        label='Algoritmo',
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    # This fied is hidden so that the user can not modify 
    # its value
    algorithm = forms.ModelChoiceField(
        label='Algoritmo',
        queryset=Algorithm.objects.all(),
        widget=forms.HiddenInput(),
    )

    name = forms.CharField(label='Nombre de la Version',max_length=200)

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
        label='Número de la Versión',
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    repository_url = forms.CharField(
        label='URL Código Fuente',max_length=200, required=True
    )
    source_storage_units = forms.ModelMultipleChoiceField(
        label='Posibles unidades de almacenamiento origen',
        queryset=StorageUnit.objects.all(), required=True
    )


class AlgorithmModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.name)

class VersionModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.number)

class ParameterForm(forms.ModelForm):

    class Meta:
        model = Parameter
        fields = [
            'show_algorthm_name',
            'algorithm',
            'show_version_number',
            'version',
            'name',
            'parameter_type',
            'description',
            'help_text',
            'position',
            'required',
            'enabled',
            'output_included',
            'default_value',
            'function_name',
        ]

    # This field only show the algorithm name to be related with the 
    # version to the user
    show_algorthm_name = forms.CharField(
        label='Algoritmo',
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    # This fied is hidden so that the user can not modify 
    # its value
    algorithm = forms.ModelChoiceField(
        label='Algoritmo',
        queryset=Algorithm.objects.all(),
        widget=forms.HiddenInput(),
    )

    # This field only show the algorithm name to be related with the 
    # version to the user
    show_version_number = forms.CharField(
        label='Numero de la Versión',
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    # This fied is hidden so that the user can not modify 
    # its value
    version = forms.ModelChoiceField(
        label='Número de la Versión',
        queryset=Version.objects.all(),
        widget=forms.HiddenInput(),
    )

    name = forms.CharField(
        label='Nombre del Parámetro',
        max_length=200
    )
    parameter_type = forms.ChoiceField(
        label='Tipo del Parámetro',
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=Parameter.PARAMETER_TYPES,
        required=True
    )
    description = forms.CharField(
        label='Descripción del Parámetro',
        required=False, 
        widget=forms.Textarea(
            attrs={
                'rows': 5, 
                'class': 'form-control',
                'placeholder': (
                    'Ingrese una descripción del significado de este parámetro ' 
                    'en la ejecución de la versión algortimo.'
                )
            }
        )
    )
    help_text = forms.CharField(
        label='Texto de Ayuda del Parámetro (Opcional)',
        required=False, 
        widget=forms.Textarea(
            attrs={
                'rows': 5, 
                'class': 'form-control',
                'placeholder': (
                    'Ingrese un texto con las ayudas y consideraciones '
                    'que deben ser tenidas en cuenta por los usuarios al '
                    'ingresar este parámetro.'
                )
            }
        )
    )
    position = forms.IntegerField(
        label='Posición',
        min_value=0, 
        required=True,
        help_text=(
            'La posición indica el orden en el que aparecerá este '
            'parámetro al momento de ejecutar la versión del algoritmo.'
        )
    )
    required = forms.BooleanField(
        label='Este Parámetro es Obligatorio',
        required=False, 
        initial=True,
        help_text = 'Si el parámetro es opcional desmarcar esta casilla.'
    )
    enabled = forms.BooleanField(
        label='Este parámetro está habilitado',
        required=False, 
        initial=True,
        help_text='Para deshabilitar este parámetro, desmarcar esta casilla. '
    )
    default_value = forms.CharField(
        label='Valor por Defecto (Opcional)',
        max_length=200, 
        required=False,
        help_text='Ingrese el valor por defecto que debe tomar este parámetro.'
    )
    function_name = forms.CharField(
        label='Nombre por Defecto en la Función',
        max_length=200,
        required=True,
        help_text='Ingrese el nombre por defecto del parámetro en la función.'
    )
    output_included = forms.BooleanField(
        label='Se incluye en la Salida',
        required=False,
        initial=True,
        help_text='Para no inluir este parámetro en la salida, desmarcar esta casilla. '
    )


def validate_py_extention(file):
    ext = os.path.splitext(file.name)[1]
    if not ext.lower() in '.py':
        raise ValidationError(u'La extensión del archivo debe ser .py')

def validate_zip_extention(file):
    ext = os.path.splitext(file.name)[1]
    if not ext.lower() in '.zip':
        raise ValidationError(u'La extensión del archivo debe ser .zip')

class VersionPublishForm(forms.Form):
    """Form to publish a version of a given algorithm."""

    # The dag .py file in a zip file which use te algorithms submited
    template = forms.FileField(
        label='Plantilla (.py)',
        validators=[validate_py_extention],
        required=True
    )
    # The .py algorithms required to execute the dag.
    algorithms = forms.FileField(
        label='Algoritmos (.zip)',
        validators=[validate_zip_extention],
        required=False
    )
