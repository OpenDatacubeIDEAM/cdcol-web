# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import Avg
from algorithm.models import Topic, Algorithm
from execution.models import *
from execution.forms import VersionSelectionForm, ReviewForm
import datetime


@login_required(login_url='/accounts/login/')
def index(request):
	current_user = request.user
	executions = Execution.objects.filter(executed_by=current_user)
	context = {'executions': executions}
	return render(request, 'execution/index.html', context)


@login_required(login_url='/accounts/login/')
def detail(request, execution_id):
	execution = get_object_or_404(Execution, id=execution_id)
	executed_params = ExecutionParameter.objects.filter(execution=execution)
	context = {'execution': execution, 'executed_params': executed_params}
	return render(request, 'execution/detail.html', context)


@login_required(login_url='/accounts/login/')
def new_blank_execution(request):
	topics = Topic.objects.all()
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
		if parameter.parameter_type == "7":
			print "Getting elements for AreaType parameter"
			sw_latitude = request.POST.get('sw_latitude', False)
			sw_longitude = request.POST.get('sw_longitude', False)
			ne_latitude = request.POST.get('ne_latitude', False)
			ne_longitude = request.POST.get('ne_longitude', False)
			print sw_latitude, sw_longitude
			print ne_latitude, ne_longitude
			# AREA TYPE
			type_params = Parameter.objects.filter(version=current_version, parameter_type='7')
			for param in type_params:
				new_execution_parameter = AreaType(
					execution=execution,
					parameter=param,
					latitude_start=sw_latitude,
					latitude_end=ne_latitude,
					longitude_start=sw_longitude,
					longitude_end=ne_longitude
				)
				new_execution_parameter.save()
		if parameter.parameter_type == "2":
			print "Getting elements for IntegerType parameter"
			integer_name = "integer_input_{}".format(parameter.id)
			integer_value = request.POST.get(integer_name, False)
			print integer_value
			# INTEGER TYPE
			type_params = Parameter.objects.filter(version=current_version, parameter_type='2')
			for param in type_params:
				new_execution_parameter = IntegerType(
					execution=execution,
					parameter=param,
					value=integer_value
				)
				new_execution_parameter.save()
		if parameter.parameter_type == "9":
			print "Getting elements for TimePeriod parameter"
			start_date_name = "start_date_{}".format(parameter.id)
			end_date_name = "end_date_{}".format(parameter.id)
			start_date_value = request.POST.get(start_date_name, False)
			end_date_value = request.POST.get(end_date_name, False)
			print start_date_value, end_date_value
			# TIME PERIOD TYPE
			type_params = Parameter.objects.filter(version=current_version, parameter_type='9')
			for param in type_params:
				new_execution_parameter = TimePeriodType(
					execution=execution,
					parameter=param,
					start_date=start_date_value,
					end_date=end_date_value
				)
				new_execution_parameter.save()
		if parameter.parameter_type == "8":
			print "Getting elements for StorageUnitType parameter"
			select_name = "storage_unit_{}".format(parameter.id)
			bands_name = "bands_{}".format(parameter.id)
			select_value = request.POST.get(select_name, False)
			print select_value
			bands_selected = request.POST.getlist(bands_name, False)
			for band in bands_selected:
				print band
			# STORAGE UNIT TYPE
			type_params = Parameter.objects.filter(version=current_version, parameter_type='8')
			for param in type_params:
				new_execution_parameter = StorageUnitType(
					execution=execution,
					parameter=param,
					value=select_value
				)
				new_execution_parameter.save()
		if parameter.parameter_type == "4":
			print "Getting elements for BooleanType parameter"
			boolean_name = "boolean_input_{}".format(parameter.id)
			boolean_value = request.POST.get(boolean_name, False)
			print boolean_value
			# BOOLEAN TYPE
			type_params = Parameter.objects.filter(version=current_version, parameter_type='4')
			for param in type_params:
				new_execution_parameter = BooleanType(
					execution=execution,
					parameter=param,
					value=boolean_value
				)
				new_execution_parameter.save()


@login_required(login_url='/accounts/login/')
def new_execution(request, algorithm_id, version_id):
	current_user = request.user
	algorithm = get_object_or_404(Algorithm, id=algorithm_id)
	current_version = None
	if version_id:
		current_version = get_object_or_404(Version, id=version_id)
	parameters = Parameter.objects.filter(version=current_version).order_by('position')
	reviews = Review.objects.filter(version=current_version)
	# getting the average rating
	average_rating = Review.objects.filter(version=current_version).aggregate(Avg('rating'))['rating__avg']
	average_rating = round(average_rating if average_rating is not None else 0, 2)
	executions = Execution.objects.filter(version=current_version)
	topics = Topic.objects.all()
	if request.method == 'POST':
		textarea_name = request.POST.get('textarea_name', False)
		started_at = datetime.datetime.now()

		new_execution = Execution(
			version=current_version,
			description=textarea_name,
			state=1,
			started_at=started_at,
			executed_by=current_user
		)
		new_execution.save()

		create_execution_parameter_objects(parameters, request, new_execution, current_version)
		return HttpResponseRedirect(reverse('execution:detail', kwargs={'execution_id': new_execution.id}))
	version_selection_form = VersionSelectionForm(algorithm_id=algorithm_id)
	context = {'topics': topics, 'algorithm': algorithm, 'parameters': parameters,
	           'version_selection_form': version_selection_form, 'version': current_version,
	           'reviews': reviews, 'average_rating': average_rating, 'executions': executions}
	return render(request, 'execution/new.html', context)


@login_required(login_url='/accounts/login/')
def rate_execution(request, execution_id):
	current_user = request.user
	execution = get_object_or_404(Execution, id=execution_id)
	if request.method == 'POST':
		# getting the form
		review_form = ReviewForm(request.POST)
		# checking if the form is valid
		if review_form.is_valid():
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
			review_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		review_form = ReviewForm()
	context = {'review_form': review_form, 'execution': execution}
	return render(request, 'execution/rate.html', context)
