# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from algorithm.models import Topic, Algorithm, Version, Parameter
from execution.models import *
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
def new_execution(request, algorithm_id):
	current_user = request.user
	algorithm = get_object_or_404(Algorithm, id=algorithm_id)
	versions = Version.objects.filter(algorithm=algorithm).order_by('-number')
	parameters = Parameter.objects.filter(version=Version.objects.last()).order_by('position')
	topics = Topic.objects.all()
	if request.method == 'POST':
		current_version = algorithm.last_version() ## TODO: Must fix this

		textarea_name = request.POST.get('textarea_name', False);
		latitude_init_name = request.POST.get('latitude_init_name', False)
		latitude_end_name = request.POST.get('latitude_end_name', False)
		longitude_init_name = request.POST.get('longitude_init_name', False)
		longitude_end_name = request.POST.get('longitude_end_name', False)
		min_pixel_name = request.POST.get('min_pixel_name', False)
		date_to_name = request.POST.get('date_to_name', False)
		date_from_name = request.POST.get('date_from_name', False)
		storage_unit_name = request.POST.get('storage_unit_name', False)
		bands_name = request.POST.get('bands_name', False)
		normalized_name = request.POST.get('normalized_name', False)
		started_at = datetime.datetime.now()

		# creating a new execution
		new_execution = Execution(
			version=current_version,
			description=textarea_name,
			state=1,
			started_at=started_at,
			executed_by=current_user
		)
		new_execution.save()

		# Creating the execution parameters by type

		# AREA TYPE
		type_params = Parameter.objects.filter(version=current_version, parameter_type='7')
		for param in type_params:
			new_execution_parameter = AreaType(
				execution=new_execution,
				parameter=param,
				latitude_start=latitude_init_name,
				latitude_end=latitude_end_name,
				longitude_start=longitude_init_name,
				longitude_end=longitude_end_name
			)
			new_execution_parameter.save()

		# INTEGER TYPE
		type_params = Parameter.objects.filter(version=current_version, parameter_type='2')
		for param in type_params:
			new_execution_parameter = IntegerType(
				execution=new_execution,
				parameter=param,
				value=min_pixel_name
			)
			new_execution_parameter.save()

		# TIME PERIOD TYPE
		type_params = Parameter.objects.filter(version=current_version, parameter_type='9')
		for param in type_params:
			new_execution_parameter = TimePeriodType(
				execution=new_execution,
				parameter=param,
				start_date=date_to_name,
				end_date=date_from_name
			)
			new_execution_parameter.save()

		# STORAGE UNIT TYPE
		type_params = Parameter.objects.filter(version=current_version, parameter_type='8')
		for param in type_params:
			new_execution_parameter = StorageUnitType(
				execution=new_execution,
				parameter=param,
				value=storage_unit_name
			)
			new_execution_parameter.save()

		# BOOLEAN TYPE
		type_params = Parameter.objects.filter(version=current_version, parameter_type='4')
		for param in type_params:
			new_execution_parameter = BooleanType(
				execution=new_execution,
				parameter=param,
				value=normalized_name
			)
			new_execution_parameter.save()


	context = {'topics': topics, 'algorithm': algorithm, 'versions': versions, 'parameters': parameters}
	return render(request, 'execution/new.html', context)