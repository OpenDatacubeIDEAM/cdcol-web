# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from algorithm.models import Topic, Algorithm, Version, Parameter
from execution.models import *
from execution.forms import VersionSelectionForm
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
			print 'formulario correcto'
		else:
			version_selection_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		version_selection_form = VersionSelectionForm(algorithm_id=algorithm_id)
	context = {'topics': topics, 'algorithm': algorithm, 'parameters': parameters,
	           'version_selection_form': version_selection_form}
	return render(request, 'execution/new.html', context)
