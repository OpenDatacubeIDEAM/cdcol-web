# -*- coding: utf-8 -*-
from django import forms
from storage.models import StorageUnit
from ingest.models import IngestTask


def custom_choices():
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


class IngestTaskForm(forms.Form):
	storage_unit = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=custom_choices,
	                                 required=True)
	comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control',
	                                                        'placeholder': 'Ingrese una descripción que le ayude a identificar la tarea de ingesta que se va a ejecutar sobre la unidad de almacenamiento'}),
	                           required=False)
