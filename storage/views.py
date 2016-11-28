# -*- coding: utf-8 -*-
import mimetypes
import os
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_str
from django.core import serializers
from .forms import StorageUnitForm
from storage.models import StorageUnit
from wsgiref.util import FileWrapper
from django.conf import settings
import re
import requests
import StringIO
import base64
import json
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""

	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


def as_json(request):
	try:
		fake_url = "http://www.mocky.io/v2/582e7d81260000c60065efc2"
		url = "{}/api/storage_units/".format(settings.API_URL)
		response = requests.get(fake_url)
		storage_units = response.json()
	except:
		storage_units = []
	return JSONResponse(storage_units)

@login_required(login_url='/accounts/login/')
def index(request):
	return render(request, 'storage/index.html')


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
	# searching the storage unit by its id
	storage_unit = get_object_or_404(StorageUnit, id=storage_unit_id)
	context = {'storage_unit': storage_unit}
	return render(request, 'storage/detail.html', context)


@login_required(login_url='/accounts/login/')
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
					"name": name,
					"description": description,
					"description_file": encoded_description,
					"ingest_file": encoded_ingest,
					"metadata_generation_script": encoded_metadata_script,
					"created_by": 1
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


def content_as_json(request, storage_unit_id):
	path = request.GET.get('path', "/years/")
	try:
		json_response = []
		url = "{}/api/storage_units/{}{}".format(settings.API_URL, storage_unit_id, path)
		if url.endswith("/years/"):
			print 'fetching years'
			fake_url = "http://www.mocky.io/v2/5838bf6511000096168fd3ca"
			response = requests.get(fake_url)
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
			response = requests.get(fake_url)
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
			response = requests.get(fake_url)
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
def view_content(request, storage_unit_id):
	storage_unit = get_object_or_404(StorageUnit, id=storage_unit_id)
	context = {'storage_unit': storage_unit}
	return render(request, 'storage/content.html', context)


@login_required(login_url='/accounts/login/')
def image_detail(request, storage_unit_id, image_name):
	url = "{}/api/storage_units/{}/contents/{}/".format(settings.API_URL, storage_unit_id, image_name)
	fake_url = "http://www.mocky.io/v2/5838bfd6110000a2168fd3cd"
	response = requests.get(fake_url)
	image_info = response.json()
	year = image_info["year"]
	coordinates = image_info["coordinates"]
	name = image_info["image_name"]
	image_storage_unit = image_info["storage_unit"]
	thumbnails = image_info["thumbnails"]
	metadata = json.dumps(image_info["metadata"], indent=4, sort_keys=True)
	context = {'metadata': metadata, 'thumbnails': thumbnails, 'year': year, 'coordinates': coordinates, 'name': name,
	           'image_storage_unit': image_storage_unit}
	return render(request, 'storage/image_detail.html', context)
