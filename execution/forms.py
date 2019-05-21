# -*- coding: utf-8 -*-

from django import forms
from django.db.models import Q
from algorithm.models import Version
from execution.models import Review
from execution.models import Execution


class VersionSelectionForm(forms.Form):
    version = forms.ModelChoiceField(queryset=None, widget=forms.Select())

    def __init__(self, *args, **kwargs):
        """
        When the form is instantiated, the user must provide the parameters
        as follows: 

        VersionSelectionForm(algorithm_id=algorithm_id, current_user=current_user)
        
        This allow to obtain the parameters in the contructor.
        """

        self.algorithm = kwargs.pop('algorithm')
        self.user = kwargs.pop('user')

        super(VersionSelectionForm, self).__init__(*args, **kwargs)

        if self.user.profile.is_workflow_reviewer:
            # The choice field will display such versions of a given algorithm
            # that are published or were created by the current user.
            self.fields['version'].queryset = Version.objects.filter(algorithm=self.algorithm)
        else:
            # The choice field will display such versions of a given algorithm
            # that are published or were created by the current user.
            self.fields['version'].queryset = Version.objects.filter(
                Q(algorithm=self.algorithm) &
                (Q(publishing_state=Version.PUBLISHED_STATE) | Q(algorithm__created_by=self.user))
            )


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            'rating', 'comments'
        ]

    REVIEW_TYPES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    # execution = forms.ModelChoiceField(
    #     label='Ejecución',
    #     queryset=Execution.objects.all(),
    #     to_field_name="name",
    #     widget=forms.TextInput(attrs={'readonly':'readonly'}),
    # )

    rating = forms.ChoiceField(
        label='Calificación',
        widget=forms.Select(
            attrs={
                'required': 'true', 
                'class': 'form-control',
                'title': (
                    'Seleccione en la escala de 1 (peor) a 5 (mejor) ' 
                    'cuál es su satisfacción de los resultados generados ' 
                    'a través de esta ejecución.'
                )
            }
        ), 
        choices=REVIEW_TYPES, 
        required=True
    )
    comments = forms.CharField(
        label='Comentarios de la calificación',
        widget=forms.Textarea(
            attrs={
                'required': 'true', 
                'rows': 5, 
                'class': 'form-control',
                'title': (
                    'Los comentarios que ingrese podrán ser vistos por '
                    'otros usuarios interesados en utilizar la versión '
                    'del algoritmo. Es importante que sea muy específico '
                    'en los resultados que logró obtener.'
                ),
                'placeholder': (
                    'Ingrese detalles de la calidad de los resultados ' 
                    'que obtuviste con la ejecución, la descripción del ' 
                    'análisis realizaste, sobre qué región lo ejecutaste, etc.'
                )
            }
        ),
       required=True
    )
