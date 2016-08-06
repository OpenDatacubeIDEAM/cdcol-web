# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CDCOLForm
from storage.models import StorageUnit, StorageUnitCDCOL


def index(request):
	current_user = request.user
	return render(request, 'storage/index.html')


def detail(request, item_id):
	print item_id
	current_user = request.user
	return render(request, 'storage/detail.html')


def new_ceos(request):
	current_user = request.user
	return render(request, 'storage/new_ceos.html')


def new_cdcol(request):
	"""
	Creates a new CDCOL Storage Unit
	:param request:
	:return:
	"""
	response = None
	# obtaining the current user
	current_user = request.user
	if request.method == 'POST':
		# getting the form
		form = CDCOLForm(request.POST, request.FILES)
		# checking if the form is valid
		if form.is_valid():
			# getting all the fields
			processing_level = form.cleaned_data['processing_level']
			detailed_processing_level = form.cleaned_data['detailed_processing_level']
			file = request.FILES['file']
			# creating the generic model
			new_storage_unit = StorageUnit(
				storage_unit_type='CDCOL',
				processing_level=processing_level,
				name='Unknown',
				file_description='Unknown',
				metadata=file,
				root_dir='/',
				created_by=current_user
			)
			new_storage_unit.save()
			# creating the CDCOL model
			new_storage_unit_cdcol = StorageUnitCDCOL(
				storage_unit=new_storage_unit,
				detailed_processing_level=detailed_processing_level
			)
			new_storage_unit_cdcol.save()
			# cleaning the form
			form = CDCOLForm()
			# setting the successs response
			response = {'status': 'Ok', 'message': 'La unidad de almacenamiento ha sido creada satisfactoriamente.'}
		else:
			form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		form = CDCOLForm()
	context = {'form': form, 'response': response}
	return render(request, 'storage/new_cdcol.html', context)
