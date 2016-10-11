# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from algorithm.models import Topic, Algorithm, StorageUnit
from execution.models import *
from execution.forms import VersionSelectionForm
from django.http import HttpResponse
from django.core import serializers


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
	data = serializers.serialize("json", Parameter.objects.filter(version__id=version_id, enabled=True))
	return HttpResponse(data, content_type='application/json')
	# return JsonResponse(data, safe=False)


@login_required(login_url='/accounts/login/')
def new_execution(request, algorithm_id, version_id=None):
	current_user = request.user
	algorithm = get_object_or_404(Algorithm, id=algorithm_id)
	if version_id:
		current_version = get_object_or_404(Version, id=version_id)
	else:
		current_version = algorithm.last_version()
	parameters = Parameter.objects.filter(version=current_version).order_by('position')
	topics = Topic.objects.all()
	if request.method == 'POST':
		version_selection_form = VersionSelectionForm(request.POST)
		if version_selection_form.is_valid():
			print 'formulario valido'
		else:
			version_selection_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		version_selection_form = VersionSelectionForm(algorithm_id=algorithm_id)
	context = {'topics': topics, 'algorithm': algorithm, 'parameters': parameters,
	           'version_selection_form': version_selection_form}
	return render(request, 'execution/new.html', context)


		#
		# textarea_name = request.POST.get('textarea_name', False);
		# latitude_init_name = request.POST.get('latitude_init_name', False)
		# latitude_end_name = request.POST.get('latitude_end_name', False)
		# longitude_init_name = request.POST.get('longitude_init_name', False)
		# longitude_end_name = request.POST.get('longitude_end_name', False)
		# min_pixel_name = request.POST.get('min_pixel_name', False)
		# date_to_name = request.POST.get('date_to_name', False)
		# date_from_name = request.POST.get('date_from_name', False)
		# storage_unit_name = request.POST.get('storage_unit_name', False)
		# bands_name = request.POST.get('bands_name', False)
		# normalized_name = request.POST.get('normalized_name', False)
		# started_at = datetime.datetime.now()
		#
		# # creating a new execution
		# new_execution = Execution(
		# 	version=current_version,
		# 	description=textarea_name,
		# 	state=1,
		# 	started_at=started_at,
		# 	executed_by=current_user
		# )
		# new_execution.save()
		#
		# # Creating the execution parameters by type
		#
		# # AREA TYPE
		# type_params = Parameter.objects.filter(version=current_version, parameter_type='7')
		# for param in type_params:
		# 	new_execution_parameter = AreaType(
		# 		execution=new_execution,
		# 		parameter=param,
		# 		latitude_start=latitude_init_name,
		# 		latitude_end=latitude_end_name,
		# 		longitude_start=longitude_init_name,
		# 		longitude_end=longitude_end_name
		# 	)
		# 	new_execution_parameter.save()
		#
		# # INTEGER TYPE
		# type_params = Parameter.objects.filter(version=current_version, parameter_type='2')
		# for param in type_params:
		# 	new_execution_parameter = IntegerType(
		# 		execution=new_execution,
		# 		parameter=param,
		# 		value=min_pixel_name
		# 	)
		# 	new_execution_parameter.save()
		#
		# # TIME PERIOD TYPE
		# type_params = Parameter.objects.filter(version=current_version, parameter_type='9')
		# for param in type_params:
		# 	new_execution_parameter = TimePeriodType(
		# 		execution=new_execution,
		# 		parameter=param,
		# 		start_date=date_to_name,
		# 		end_date=date_from_name
		# 	)
		# 	new_execution_parameter.save()
		#
		# # STORAGE UNIT TYPE
		# type_params = Parameter.objects.filter(version=current_version, parameter_type='8')
		# for param in type_params:
		# 	new_execution_parameter = StorageUnitType(
		# 		execution=new_execution,
		# 		parameter=param,
		# 		value=storage_unit_name
		# 	)
		# 	new_execution_parameter.save()
		#
		# # BOOLEAN TYPE
		# type_params = Parameter.objects.filter(version=current_version, parameter_type='4')
		# for param in type_params:
		# 	new_execution_parameter = BooleanType(
		# 		execution=new_execution,
		# 		parameter=param,
		# 		value=normalized_name
		# 	)
		# 	new_execution_parameter.save()