# -*- coding: utf-8 -*-
import mimetypes
import os
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.encoding import smart_str
from django.core import serializers
from .forms import StorageUnitForm
from .forms import StorageUnitUpdateForm
from storage.models import StorageUnit
from wsgiref.util import FileWrapper
from django.conf import settings
import re
import requests
import StringIO
import base64
import json
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound


class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""

	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def as_json(request):
	try:
		storage_unit_id = request.POST.get('storage_unit_id', None)
		if storage_unit_id:
			fake_url = "http://www.mocky.io/v2/58409450100000e60f3582bb"
			url = "{}/api/storage_units/{}/".format(settings.API_URL, storage_unit_id)
		else:
			fake_url = "http://www.mocky.io/v2/582e7d81260000c60065efc2"
			url = "{}/api/storage_units/".format(settings.API_URL)
		response = requests.get(url)
		storage_units = response.json()
	except:
		storage_units = []
	return JSONResponse(storage_units)


@login_required(login_url='/accounts/login/')
@permission_required('storage.can_list_units', raise_exception=True)
def index(request):
	return render(request, 'storage/index.html')


@permission_required('storage.can_download_file', raise_exception=True)
def download_file(request, storage_unit_id, download_type):
	"""
	Download a file
	:param request:
	:param full_file_name:
	:return:
	"""
	storage_unit = get_object_or_404(StorageUnit, id=storage_unit_id)
	if download_type == "description":
		full_file_name = "{}/{}/{}".format(settings.DC_STORAGE_PATH, storage_unit.name, storage_unit.description_file)
	elif download_type == "ingest":
		full_file_name = "{}/{}/{}".format(settings.DC_STORAGE_PATH, storage_unit.name, storage_unit.ingest_file)
	elif download_type == "script":
		full_file_name = "{}/{}/{}".format(settings.DC_STORAGE_PATH, storage_unit.name, storage_unit.metadata_generation_script)
	else:
		return HttpResponseBadRequest()
	try:
		split_file_name = full_file_name.split('/')
		file_name = split_file_name[len(split_file_name) - 1]
		file_path = full_file_name
		file_wrapper = FileWrapper(file(file_path, 'rb'))
		file_mimetype = mimetypes.guess_type(file_path)
		response = HttpResponse(file_wrapper, content_type=file_mimetype)
		response['X-Sendfile'] = file_path
		response['Content-Length'] = os.stat(file_path).st_size
		response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
		return response
	except:
		return HttpResponseNotFound('<h1>El archivo no se ha encontrado en el servidor</h1>')


@permission_required('storage.can_download_file', raise_exception=True)
def download_image(request, storage_unit_id, image_name):
	"""
	Download an image
	:param request:
	:param file_name:
	:return:
	"""
	# calling the service
	url = "{}/api/storage_units/{}/contents/{}/".format(settings.API_URL, storage_unit_id, image_name)
	fake_url = "http://www.mocky.io/v2/5838bfd6110000a2168fd3cd"
	response = requests.get(url)
	image_info = response.json()
	# downloading the file
	try:
		# file_path = "/Users/manre/Documents/code/v_ideam/projects/ideam_cdc/ideam_cdc/media_root/uploads/versions/source_code/2/admin.py"
		file_path = image_info["image_uri"]
		file_name = file_path.split('/')[-1]
		file_wrapper = FileWrapper(file(file_path, 'rb'))
		file_mimetype = mimetypes.guess_type(file_path)
		response = HttpResponse(file_wrapper, content_type=file_mimetype)
		response['X-Sendfile'] = file_path
		response['Content-Length'] = os.stat(file_path).st_size
		response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
		return response
	except:
		return HttpResponseNotFound('<h1>El archivo no se ha encontrado en el servidor</h1>')


@permission_required('storage.can_download_metadata', raise_exception=True)
def download_metadata(request, storage_unit_id, image_name):
	"""
	Download metadata from an image file
	:param request:
	:param file_name:
	:return:
	"""
	url = "{}/api/storage_units/{}/contents/{}/".format(settings.API_URL, storage_unit_id, image_name)
	fake_url = "http://www.mocky.io/v2/5838bfd6110000a2168fd3cd"
	response = requests.get(url)
	image_info = response.json()
	metadata = json.dumps(image_info["metadata"], indent=4, sort_keys=True)
	return HttpResponse(metadata, content_type='application/json')


@login_required(login_url='/accounts/login/')
@permission_required('storage.can_view_unit_detail', raise_exception=True)
def detail(request, storage_unit_id):
	# searching the storage unit by its id
	storage_unit = get_object_or_404(StorageUnit, id=storage_unit_id)
	context = {'storage_unit': storage_unit}
	return render(request, 'storage/detail.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('storage.can_create_units', raise_exception=True)
def new(request):
	response = None
	# obtaining the current user
	current_user = request.user
	if request.method == 'POST':
		# getting the form
		form = StorageUnitForm(request.POST, request.FILES)
		# checking if the form is valid
		if form.is_valid():
			# getting all the fields
			alias = form.cleaned_data['alias']
			name = form.cleaned_data['name']
			description = form.cleaned_data['description']
			description_file = request.FILES['description_file']
			ingest_file = request.FILES['ingest_file']
			metadata_generation_script_file = request.FILES['metadata_generation_script']
			# encoding the files
			try:
				# encoding the description file
				strio = StringIO.StringIO()
				base64.encode(description_file, strio)
				encoded_description = strio.getvalue().replace('\n', '\\\\n')
				# encoding the ingest file
				strio = StringIO.StringIO()
				base64.encode(ingest_file, strio)
				encoded_ingest = strio.getvalue().replace('\n', '\\\\n')
				# encoding the metadata generation file
				strio = StringIO.StringIO()
				base64.encode(metadata_generation_script_file, strio)
				encoded_metadata_script = strio.getvalue().replace('\n', '\\\\n')
			except:
				print 'Something went wrong when encoding the files'
			try:
				data = {
					"alias":alias,
					"name": name,
					"description": description,
					"description_file": encoded_description,
					"ingest_file": encoded_ingest,
					"metadata_generation_script": encoded_metadata_script,
					"created_by": current_user.id
				}
				header = {'Content-Type': 'application/json'}
				url = "{}/api/storage_units/".format(settings.API_URL)
				r = requests.post(url, data=json.dumps(data), headers=header)
				if r.status_code == 201:
					return HttpResponseRedirect(reverse('storage:index'))
				else:
					print r.status_code, r.text
					form.add_error(None, "Ha ocurrido un error con el envío de la información, por favor vuelve a intentarlo.")
			except:
				print 'Something went wrong when trying to call the REST service'
		else:
			form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		form = StorageUnitForm()
	context = {'form': form, 'response': response}
	return render(request, 'storage/new.html', context)


@login_required(login_url='/accounts/login/')
def obtain_storage_units(request):
	data = serializers.serialize("json", StorageUnit.objects.all())
	return HttpResponse(data, content_type='application/json')


@permission_required('storage.can_view_storage_content', raise_exception=True)
def content_as_json(request, storage_unit_id):
	path = request.GET.get('path', "/years/")
	try:
		json_response = []
		url = "{}/api/storage_units/{}{}".format(settings.API_URL, storage_unit_id, path)
		if url.endswith("/years/"):
			print 'fetching years'
			fake_url = "http://www.mocky.io/v2/5838bf6511000096168fd3ca"
			response = requests.get(url)
			entries = response.json()["years"]
			for entry in entries:
				json_object = {
					'name': "{}".format(entry),
					'is_dir': True,
					'is_file': False,
				}
				json_response.append(json_object)
		elif re.search('years/([0-9]*)/$', url):
			print 'fetching coordinates'
			fake_url = "http://www.mocky.io/v2/5838bf921100009c168fd3cb"
			response = requests.get(url)
			entries = response.json()["coordinates"]
			for entry in entries:
				json_object = {
					'name': "{}".format(str(entry["longitude"]) + "_" + str(entry["latitude"])),
					'is_dir': True,
					'is_file': False,
				}
				json_response.append(json_object)
		else:
			print 'fetching images'
			fake_url = "http://www.mocky.io/v2/5838bfb51100009d168fd3cc"
			response = requests.get(url)
			entries = response.json()["images"]
			for entry in entries:
				json_object = {
					'name': "{}".format(entry),
					'is_dir': False,
					'is_file': True,
				}
				json_response.append(json_object)
		return JSONResponse(json_response)
	except:
		return HttpResponseBadRequest()


@login_required(login_url='/accounts/login/')
@permission_required('storage.can_view_storage_content', raise_exception=True)
def view_content(request, storage_unit_id):
	storage_unit = get_object_or_404(StorageUnit, id=storage_unit_id)
	context = {'storage_unit': storage_unit}
	return render(request, 'storage/content.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('storage.can_view_content_detail', raise_exception=True)
def image_detail(request, storage_unit_id, image_name):
	url = "{}/api/storage_units/{}/contents/{}/".format(settings.API_URL, storage_unit_id, image_name)
	fake_url = "http://www.mocky.io/v2/5838bfd6110000a2168fd3cd"
	response = requests.get(url)
	image_info = response.json()
	year = image_info["year"]
	coordinates = image_info["coordinates"]
	name = image_info["image_name"]
	storage_unit_alias = image_info["storage_unit_alias"]
	image_storage_unit = image_info["storage_unit"]
	thumbnails = image_info["thumbnails"]
	metadata = json.dumps(image_info["metadata"], indent=4, sort_keys=True)
	context = {'metadata': metadata, 'thumbnails': thumbnails, 'year': year, 'coordinates': coordinates, 'name': name,
	           'image_storage_unit': image_storage_unit, 'storage_unit_alias': storage_unit_alias,'image_name': image_name, 'storage_unit_id': storage_unit_id}
	return render(request, 'storage/image_detail.html', context)

@login_required(login_url='/accounts/login')
def update(request, storage_unit_id):
	current_user=request.user
	storage=get_object_or_404(StorageUnit, id=storage_unit_id)
	if request.method == 'POST':
		storage_form=StorageUnitUpdateForm(request.POST)
		if storage_form.is_valid():
			field_alias = storage_form.cleaned_data['alias']
			storage.alias = field_alias
			storage.save()
			return HttpResponseRedirect(reverse('storage.detail', kwargs={'storage_unit_id': storage_unit_id}))
		else:
			storage_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		storage_form = StorageUnitUpdateForm()

	context = {'storage_form': storage_form, 'algorithm': storage}
	return render(request, 'storage/update.html', context)
