# -*- coding: utf-8 -*-
import mimetypes
import os
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from .forms import CDCOLForm, CEOSForm
from storage.models import StorageUnit, StorageUnitCDCOL, StorageUnitCEOS
from wsgiref.util import FileWrapper


@login_required(login_url='/accounts/login/')
def index(request):
	current_user = request.user
	storage_units = StorageUnit.objects.all()
	context = {'storage_units': storage_units}
	return render(request, 'storage/index.html', context)


def download_file(request, file_name):
	"""
	Download a file
	:param request:
	:param file_name:
	:return:
	"""
	file_path = file_name
	file_wrapper = FileWrapper(file(file_path, 'rb'))
	file_mimetype = mimetypes.guess_type(file_path)
	response = HttpResponse(file_wrapper, content_type=file_mimetype)
	response['X-Sendfile'] = file_path
	response['Content-Length'] = os.stat(file_path).st_size
	response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
	return response


@login_required(login_url='/accounts/login/')
def detail(request, storage_unit_id):
	storage_unit_ceos = None
	# searching the storage unit by its id
	storage_unit_detail = get_object_or_404(StorageUnit, id=storage_unit_id)
	if storage_unit_detail.storage_unit_type == 'CEOS':
		storage_unit_ceos = StorageUnitCEOS.objects.get(storage_unit__id=storage_unit_detail.id)
	context = {'storage_unit_detail': storage_unit_detail, 'storage_unit_ceos': storage_unit_ceos }
	print context
	return render(request, 'storage/detail.html', context)


@login_required(login_url='/accounts/login/')
def new_ceos(request):
	response = None
	# obtaining the current user
	current_user = request.user
	# fetching all the CDCOL storage units
	cdcol_storage_units = StorageUnitCDCOL.objects.all()
	if request.method == 'POST':
		# getting the form
		form = CEOSForm(request.POST, request.FILES)
		# checking if the form is valid
		if form.is_valid():
			# getting all the fields
			source_storage_unit = form.cleaned_data['source_storage_unit']
			description_file = request.FILES['description_file']
			ingest_file = request.FILES['ingest_file']
			# getting the storage unit
			source_storage_unit = StorageUnit.objects.get(id=source_storage_unit)
			# creating the generic model
			new_storage_unit = StorageUnit(
				storage_unit_type='CEOS',
				processing_level='Unknown',
				name='CEOS - Unknown',
				file_description='Unknown',
				metadata=description_file,
				root_dir='/',
				created_by=current_user
			)
			new_storage_unit.save()
			# creating the CEOS model
			new_storage_unit_ceos = StorageUnitCEOS(
				storage_unit=new_storage_unit,
				source_storage_unit=source_storage_unit,
				file_feed=ingest_file
			)
			new_storage_unit_ceos.save()
			# cleaning the form
			form = CEOSForm()
			# setting the successs response
			response = {'status': 'Ok', 'message': 'La unidad de almacenamiento ha sido creada satisfactoriamente.'}
		else:
			form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		form = CEOSForm()
	context = {'form': form, 'cdcol_storage_units': cdcol_storage_units, 'response': response}
	return render(request, 'storage/new_ceos.html', context)


@login_required(login_url='/accounts/login/')
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
			# TODO: What happend if there is an error and cant create the second StorageUnit?
			new_storage_unit = StorageUnit(
				storage_unit_type='CDCOL',
				processing_level=processing_level,
				name='CDCOL - Unknown',
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
