# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Avg, Q
from django.utils.encoding import smart_str
from algorithm.models import Topic, Algorithm
from execution.models import *
from execution.forms import VersionSelectionForm, ReviewForm
from execution.serializers import ExecutionSerializer
import datetime
from storage.models import StorageUnit
from rest_framework.renderers import JSONRenderer
from django.conf import settings
import requests
import json
import os , zipfile
import mimetypes
from wsgiref.util import FileWrapper
from slugify import slugify


class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""

	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


def as_json(request):
	current_user = request.user
	queryset = Execution.objects.filter(executed_by=current_user)
	serializer = ExecutionSerializer(queryset, many=True)
	return JSONResponse(serializer.data)


@login_required(login_url='/accounts/login/')
@permission_required('execution.can_list_executions', raise_exception=True)
def index(request):
	current_user = request.user
	executions = Execution.objects.filter(Q(executed_by=current_user), Q(state=Execution.ENQUEUED_STATE))
	# getting temporizer value
	temporizer_value = settings.IDEAM_TEMPORIZER
	context = {'executions': executions, 'temporizer_value': temporizer_value}
	return render(request, 'execution/index.html', context)


def download_result(request, execution_id, image_name):
	execution = get_object_or_404(Execution, id=execution_id)
	try:
		file_path = "{}/results/{}/{}".format(settings.WEB_STORAGE_PATH, execution.id, image_name)
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


def get_detail_context(execution_id):
	execution = get_object_or_404(Execution, id=execution_id)
	executed_params = ExecutionParameter.objects.filter(execution=execution)
	review = Review.objects.filter(execution=execution).last()
	# getting the files from the filesystem
	system_path = "{}/results/{}/".format(settings.WEB_STORAGE_PATH, execution.id)
	files = []
	try:
		for f in os.listdir(system_path):
			if ".tiff" not in f:
				files.append(f)
	except:
		pass
	# getting current executions
	current_executions = execution.pending_executions
	# getting temporizer value
	temporizer_value = settings.IDEAM_TEMPORIZER
	# getting the delete time
	delete_hours = int(settings.DAYS_ELAPSED_TO_DELETE_EXECUTION_RESULTS) * 24
	if execution.finished_at:
		delete_time = execution.finished_at + datetime.timedelta(hours=delete_hours)
	else:
		delete_time = None
	context = {'execution': execution, 'executed_params': executed_params, 'review': review, 'files': files,
	           'current_executions': current_executions, 'temporizer_value': temporizer_value, 'delete_time': delete_time,
	           'system_path': system_path}
	return context


def generate_geotiff(request, execution_id, image_name):
	execution = get_object_or_404(Execution, id=execution_id)
	file_path = "{}/results/{}/{}".format(settings.WEB_STORAGE_PATH, execution.id, image_name)
	# creating the json request
	json_request = {
		'file_path': file_path
	}
	# sending the request
	try:
		response_message = None
		header = {'Content-Type': 'application/json'}
		url = "{}/api/download_geotiff/".format(settings.API_URL)
		# url = "http://www.mocky.io/v2/587e480e100000c114987d96" # 200
		# url = "http://www.mocky.io/v2/587e47b2100000ca14987d95" # 400
		r = requests.post(url, data=json.dumps(json_request), headers=header)
		print r #delete
		json_response = r.json()
		print json_response #delete
		if r.status_code == 200:
			print '200...' # delete
			response_file_path = json_response["file_path"]
			print response_file_path
			if response_file_path:
				file_name = response_file_path.split('/')[-1]
				return download_result(request, execution_id, file_name)
		else:
			print '400...'
			response_message = json_response["message"]
		# setting all the context
		context = get_detail_context(execution_id)
		context['response_message'] = response_message
		return render(request, 'execution/detail.html', context)
	except Exception, e:
		print e
		return HttpResponseNotFound('<h1>Ha ocurrido un error en la conversión</h1>')


@login_required(login_url='/accounts/login/')
@permission_required('execution.can_view_execution_detail', raise_exception=True)
def detail(request, execution_id):
	context = get_detail_context(execution_id)
	return render(request, 'execution/detail.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('execution.can_view_blank_execution', raise_exception=True)
def new_blank_execution(request):
	topics = Topic.objects.filter(enabled=True)
	context = {'topics': topics}
	return render(request, 'execution/new_blank.html', context)


@login_required(login_url='/accounts/login/')
def obtain_parameters(request, version_id):
	data = serializers.serialize(
		"json", Parameter.objects.filter(version__id=version_id, enabled=True).order_by('position'))
	return HttpResponse(data, content_type='application/json')


def create_execution_parameter_objects(parameters, request, execution, current_version):
	"""
	Creates an execution parameter based on the parameter type
	:param parameters: The parameters of the version
	:param request: The HTTP request object
	:return:
	"""
	for parameter in parameters:
		if parameter.parameter_type == "1":
			print "Getting elements for String parameter"
			string_name = "string_input_{}".format(parameter.id)
			string_value = request.POST.get(string_name, False)
			# STRING TYPE
			new_execution_parameter = StringType(
				execution=execution,
				parameter=parameter,
				value=string_value
			)
			new_execution_parameter.save()
		if parameter.parameter_type == "2":
			print "Getting elements for Integer parameter"
			integer_name = "integer_input_{}".format(parameter.id)
			integer_value = request.POST.get(integer_name, False)
			# INTEGER TYPE
			new_execution_parameter = IntegerType(
				execution=execution,
				parameter=parameter,
				value=integer_value
			)
			new_execution_parameter.save()
		if parameter.parameter_type == "3":
			print "Getting elements for Double parameter"
			double_name = "double_input_{}".format(parameter.id)
			double_value = request.POST.get(double_name, False)
			# DOUBLE TYPE
			new_execution_parameter = DoubleType(
				execution=execution,
				parameter=parameter,
				value=double_value
			)
			new_execution_parameter.save()
		if parameter.parameter_type == "4":
			print "Getting elements for BooleanType parameter"
			boolean_name = "boolean_input_{}".format(parameter.id)
			boolean_value = request.POST.get(boolean_name, False)
			# BOOLEAN TYPE
			new_execution_parameter = BooleanType(
				execution=execution,
				parameter=parameter,
				value=boolean_value
			)
			new_execution_parameter.save()
		if parameter.parameter_type == "7":
			print "Getting elements for AreaType parameter"
			sw_latitude = request.POST.get('sw_latitude', False)
			sw_longitude = request.POST.get('sw_longitude', False)
			ne_latitude = request.POST.get('ne_latitude', False)
			ne_longitude = request.POST.get('ne_longitude', False)
			# AREA TYPE
			new_execution_parameter = AreaType(
				execution=execution,
				parameter=parameter,
				latitude_start=sw_latitude,
				latitude_end=ne_latitude,
				longitude_start=sw_longitude,
				longitude_end=ne_longitude
			)
			new_execution_parameter.save()
		if parameter.parameter_type == "8":
			print "Getting elements for StorageUnitType (Bands) parameter"
			select_name = "storage_unit_{}".format(parameter.id)
			bands_name = "bands_{}".format(parameter.id)
			select_value = request.POST.get(select_name, False)
			select_value = StorageUnit.objects.get(pk=select_value)
			bands_selected = request.POST.getlist(bands_name, False)
			bands = ""
			for band in bands_selected:
				bands += band + ","
			bands = bands[:-1]
			# STORAGE UNIT BAND TYPE
			new_execution_parameter = StorageUnitBandType(
				execution=execution,
				parameter=parameter,
				storage_unit_name=select_value.name,
				bands=bands
			)
			new_execution_parameter.save()
		if parameter.parameter_type == "9":
			print "Getting elements for TimePeriod parameter"
			start_date_name = "start_date_{}".format(parameter.id)
			end_date_name = "end_date_{}".format(parameter.id)
			start_date_value = request.POST.get(start_date_name, False)
			end_date_value = request.POST.get(end_date_name, False)
			# parsing dates
			start_date_value = datetime.datetime.strptime(start_date_value, "%d/%m/%Y")
			end_date_value = datetime.datetime.strptime(end_date_value, "%d/%m/%Y")
			# TIME PERIOD TYPE
			new_execution_parameter = TimePeriodType(
				execution=execution,
				parameter=parameter,
				start_date=start_date_value,
				end_date=end_date_value
			)
			new_execution_parameter.save()
		if parameter.parameter_type == "12":
			print "Getting elements for File parameter"
			file_name = "file_input_{}".format(parameter.id)
			file_value = request.FILES.get(file_name, False)
			# FILE TYPE
			new_execution_parameter = FileType(
				execution=execution,
				parameter=parameter,
				file=file_value
			)
			new_execution_parameter.save()
		if parameter.parameter_type == "13":
			print "Getting elements for StorageUnitType (NoBands) parameter"
			select_name = "storage_unit_{}".format(parameter.id)
			select_value = request.POST.get(select_name, False)
			select_value = StorageUnit.objects.get(pk=select_value)
			# STORAGE UNIT NO BAND TYPE
			new_execution_parameter = StorageUnitNoBandType(
				execution=execution,
				parameter=parameter,
				storage_unit_name=select_value.name
			)
			new_execution_parameter.save()


def send_execution(execution):
	"""
	Create a json request and send it to the REST service
	:param execution: Execution to be send
	:return:
	"""
	response = {}
	parameters = ExecutionParameter.objects.filter(execution=execution)
	# getting all the values
	json_parameters = {}
	for parameter in parameters:
		json_parameters[parameter.parameter.function_name] = parameter.obtain_json_values()
	# building the request
	json_response = {
		'execution_id': execution.id,
		'algorithm_name': "{}".format(slugify(execution.version.algorithm.name)),
		'version_id': "{}".format(execution.version.number),
		'parameters': json_parameters,
		'is_gif': False
	}
	# sending the request
	try:
		header = {'Content-Type': 'application/json'}
		if execution.version.algorithm.id == int(settings.IDEAM_ID_ALGORITHM_FOR_CUSTOM_SERVICE):
			json_response['is_gif'] = True
		url = "{}/api/new_execution/".format(settings.API_URL)
		r = requests.post(url, data=json.dumps(json_response), headers=header)
		if r.status_code == 201:
			response = {'status': 'ok', 'description': 'Se envió la ejecución correctamente.'}
		else:
			response = {'status': 'error', 'description': 'Ocurrió un error al enviar la ejecución',
			            'detalle': "{}, {}".format(r.status_code, r.text)}
	except:
		print 'Something went wrong when trying to call the REST service'
	return response


@login_required(login_url='/accounts/login/')
@permission_required(('execution.can_create_new_execution', 'execution.can_view_new_execution'), raise_exception=True)
def new_execution(request, algorithm_id, version_id):
	current_user = request.user
	algorithm = get_object_or_404(Algorithm, id=algorithm_id)
	current_version = None
	if version_id:
		current_version = get_object_or_404(Version, id=version_id)
	parameters = Parameter.objects.filter(version=current_version, enabled=True).order_by('position')
	reviews = Review.objects.filter(version=current_version)
	# getting the average rating
	average_rating = Review.objects.filter(version=current_version).aggregate(Avg('rating'))['rating__avg']
	average_rating = round(average_rating if average_rating is not None else 0, 2)
	executions = Execution.objects.filter(version=current_version)
	topics = Topic.objects.filter(enabled=True)
	if request.method == 'POST':
		textarea_name = request.POST.get('textarea_name', None)
		started_at = datetime.datetime.now()

		if current_user.has_perm('execution.can_create_new_execution'):
			new_execution = Execution(
				version=current_version,
				description=textarea_name,
				state=Execution.ENQUEUED_STATE,
				started_at=started_at,
				executed_by=current_user
			)
			new_execution.save()

			create_execution_parameter_objects(parameters, request, new_execution, current_version)
			# send the execution to the REST service
			response = send_execution(new_execution)
			# Unzip uploaded parameters
			execution_directory = "/".join(settings.MEDIA_ROOT, 'input', new_execution.id)
			directories_of_file_parameters = [ directory for directory in os.listdir(execution_directory) if os.path.isdir(directory)]

			for directory in directories_of_file_parameters:
				zip_file = os.listdir(directory)[0]
				if zip_file.endswith('.zip'):
					with ZipFile(zip_file) as file_to_unzip:
						file_to_unzip.extractall()
					os.remove(zip_file)

			print response
			return HttpResponseRedirect(reverse('execution:detail', kwargs={'execution_id': new_execution.id}))
	version_selection_form = VersionSelectionForm(algorithm_id=algorithm_id, current_user=current_user)
	context = {'topics': topics, 'algorithm': algorithm, 'parameters': parameters,
	           'version_selection_form': version_selection_form, 'version': current_version,
	           'reviews': reviews, 'average_rating': average_rating, 'executions': executions}
	return render(request, 'execution/new.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('execution.can_rate_execution', raise_exception=True)
def rate_execution(request, execution_id):
	current_user = request.user
	execution = get_object_or_404(Execution, id=execution_id)
	if request.method == 'POST':
		# getting the form
		review_form = ReviewForm(request.POST)
		# checking if the form is valid
		if review_form.is_valid():
			# checking if the execution is able to be rated
			ratings = Review.objects.filter(execution=execution, reviewed_by=current_user)
			if ratings.count() == 0:
				if execution.state == Execution.COMPLETED_STATE or execution.state == Execution.ERROR_STATE:
					rating = review_form.cleaned_data['rating']
					comments = review_form.cleaned_data['comments']
					version = execution.version
					algorithm = version.algorithm

					# creating the review
					new_review = Review(
						algorithm=algorithm,
						version=version,
						execution=execution,
						rating=rating,
						comments=comments,
						reviewed_by=current_user
					)
					new_review.save()
					return HttpResponseRedirect(reverse('execution:index'))
				else:
					review_form.add_error(None, "No es posible calificar esta ejecución, la ejecución debe haber terminado.")
			else:
				review_form.add_error(None, "No es posible calificar esta ejecución, usted ya ha realizado una calificación a esta.")
		else:
			review_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		review_form = ReviewForm()
	context = {'review_form': review_form, 'execution': execution}
	return render(request, 'execution/rate.html', context)
