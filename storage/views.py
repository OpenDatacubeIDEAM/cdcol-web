# -*- coding: utf-8 -*-
import mimetypes
import os
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
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
		response = requests.get(url)
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


@login_required(login_url='/accounts/login/')
def view_content(request, storage_unit_id, path):
	dirs = set()
	files = set()
	url = "{}/api/storage_units/{}/{}".format(settings.API_URL, storage_unit_id, path)
	print "primera url", url
	if url.endswith("/years/"):
		print "anio_url=", url
		fake_url = "http://www.mocky.io/v2/582b77b3280000401d53c4ac"
		response = requests.get(url)
		entries = response.json()["years"]
		for entry in entries:
			dirs.add(entry + "/")
	elif re.search('years/([0-9]*)/$', url):
		print "cordenada_urls=", url
		fake_url = "http://www.mocky.io/v2/582b7c37280000bf1d53c4b9"
		response = requests.get(url)
		entries = response.json()["coordinates"]
		for entry in entries:
			entry = entry["longitude"] + "_" + entry["latitude"] + "/"
			dirs.add(entry)
	else:
		print "archivos_url=", url
		fake_url = "http://www.mocky.io/v2/582b7ec9280000f41d53c4be"
		response = requests.get(url)
		entries = response.json()["images"]
		for entry in entries:
			files.add(entry + "/")
	storage_unit = get_object_or_404(StorageUnit, id=storage_unit_id)
	context = {'storage_unit': storage_unit, 'dirs': dirs, 'files': files, 'selected_path': path}
	return render(request, 'storage/content.html', context)


