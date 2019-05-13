# -*- coding: utf-8 -*-

from django import forms
from django.shortcuts import get_object_or_404

from storage.models import StorageUnit
from ingest.models import IngestTask


def custom_choices():
    """
    Return the list of storage units available to perform an ingestion task
    If an ingestion task is already scheduled and it has not been finished
    on the given storage unit, this storage unit is not considered in the list.
    """
    response = []
    storage_units = StorageUnit.objects.all()
    for su in storage_units:
        last_task = IngestTask.objects.filter(storage_unit=su).last()
        if last_task:
            has_error = True if int(last_task.state) == int(IngestTask.FAILED_STATED) else False
            is_available = True if int(last_task.state) == int(IngestTask.COMPLETED_STATE) or int(
                last_task.state) == int(IngestTask.FAILED_STATED) else False
            if has_error:
                response.append((su.id, su.name + " (Última tarea con error)".decode('utf-8')))
            elif is_available:
                response.append((su.id, su.name))
        else:
            response.append((su.id, su.name))
    return response


class TaskForm(forms.ModelForm):

    class Meta:
        model = IngestTask
        fields = [
            'storage_unit','comments'
        ]

    storage_unit = forms.ChoiceField(
        label= 'Unidad de Almacenamiento',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': (
                    'Seleccione la unidad de almacenamiento '
                    'sobre la cuál desea ejecutar el proceso '
                    'de ingesta.'
                )
            }
        ), 
        choices=custom_choices,
        required=True
    )
    comments = forms.CharField(
        label='Observaciones',
        widget=forms.Textarea(
            attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': (
                    'Ingrese una descripción que le ayude a ' 
                    'identificar la tarea de ingesta que se ' 
                    'va a ejecutar sobre la unidad de almacenamiento.'
                )
            }
        ),
        required=False)

    def clean_storage_unit(self):
        """
        Replace the id of the storage unit for the instance 
        corresponding for the id.
        """
        storage_unit_id = self.cleaned_data['storage_unit']
        storage_unit = get_object_or_404(StorageUnit,pk=storage_unit_id)
        return storage_unit
