# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from algorithm.models import Algorithm, Topic, AlgorithmStorageUnit, Version, Parameter
from storage.models import StorageUnit
from algorithm.forms import AlgorithmForm, AlgorithmUpdateForm, VersionForm, VersionUpdateForm, NewParameterForm


@login_required(login_url='/accounts/login/')
def index(request):
	current_user = request.user
	algorithms = Algorithm.objects.filter(created_by=current_user)
	context = {'algorithms': algorithms}
	return render(request, 'algorithm/index.html', context)


@login_required(login_url='/accounts/login/')
def new(request):
	current_user = request.user
	topics = Topic.objects.all()
	source_storage_units = StorageUnit.objects.all()
	if request.method == 'POST':
		# getting the form
		algorithm_form = AlgorithmForm(request.POST)
		# checking if the form is valid
		if algorithm_form.is_valid():
			field_topic = algorithm_form.cleaned_data['topic']
			field_name = algorithm_form.cleaned_data['name']
			field_description = algorithm_form.cleaned_data['description']
			field_source_storage_units = algorithm_form.cleaned_data['source_storage_units']
			# creating the new algorithm
			new_algorithm = Algorithm(
				name=field_name,
				description=field_description,
				topic=field_topic,
				created_by=current_user
			)
			new_algorithm.save()
			# creating the relation with the storage units
			for source_storage_unit in field_source_storage_units:
				new_algorithm_relation = AlgorithmStorageUnit(
					algorithm=new_algorithm,
					storage_unit=source_storage_unit
				)
				new_algorithm_relation.save()
			# creating the base version
			new_algorithm_version = Version(
				algorithm=new_algorithm,
				description='Versión por defecto 1.0',
				number='1.0',
				source_code='',
				publishing_state='En Desarrollo',
				created_by=current_user
			)
			new_algorithm_version.save()
			return HttpResponseRedirect(reverse('algorithm:index'))
		else:
			algorithm_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		algorithm_form = AlgorithmForm()
	context = {'algorithm_form': algorithm_form, 'topics': topics, 'source_storage_units': source_storage_units}
	return render(request, 'algorithm/new.html', context)


@login_required(login_url='/accounts/login/')
def update(request, algorithm_id):
	source_storage_units = StorageUnit.objects.all()
	algorithm = get_object_or_404(Algorithm, id=algorithm_id)
	selected_storage_units = algorithm.source_storage_units.all()
	if request.method == 'POST':
		# getting the form
		algorithm_form = AlgorithmUpdateForm(request.POST)
		# checking if the form is valid
		if algorithm_form.is_valid():
			field_name = algorithm_form.cleaned_data['name']
			field_description = algorithm_form.cleaned_data['description']
			field_source_storage_units = algorithm_form.cleaned_data['source_storage_units']
			# update the algorithm
			algorithm.name = field_name
			algorithm.description = field_description
			algorithm.save()
			# deleting all the source storage units associations
			algorithm_associations = AlgorithmStorageUnit.objects.filter(algorithm_id=algorithm.id)
			for association in algorithm_associations:
				association.delete()
			# creating all the new associations
			for source_storage_unit in field_source_storage_units:
				new_algorithm_relation = AlgorithmStorageUnit(
					algorithm=algorithm,
					storage_unit=source_storage_unit
				)
				new_algorithm_relation.save()
			return HttpResponseRedirect(reverse('algorithm:index'))
		else:
			algorithm_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		algorithm_form = AlgorithmUpdateForm()
	context = {'algorithm_form': algorithm_form, 'source_storage_units': source_storage_units,
	           'selected_storage_units': selected_storage_units,
	           'algorithm': algorithm}
	return render(request, 'algorithm/update.html', context)


@login_required(login_url='/accounts/login/')
def detail(request, algorithm_id):
	algorithm = get_object_or_404(Algorithm, id=algorithm_id)
	storage_units = AlgorithmStorageUnit.objects.filter(algorithm_id=algorithm_id)
	versions = Version.objects.filter(algorithm_id=algorithm_id)
	context = {'algorithm': algorithm, 'storage_units': storage_units, 'versions': versions}
	return render(request, 'algorithm/detail.html', context)


@login_required(login_url='/accounts/login/')
def new_version(request, algorithm_id):
	current_user = request.user
	algorithm = get_object_or_404(Algorithm, id=algorithm_id)
	current_version = algorithm.last_version()
	new_minor_version_number = current_version.new_minor_version()
	new_major_version_number = current_version.new_major_version()
	if request.method == 'POST':
		# getting the form
		version_form = VersionForm(request.POST)
		# checking if the form is valid
		if version_form.is_valid():
			description = version_form.cleaned_data['description']
			version_number = version_form.cleaned_data['number']
			source_code = version_form.cleaned_data['source_code']
			# reading the version
			version_number = new_minor_version_number if version_number == "1" else new_major_version_number
			# creating the new version
			new_algorithm_version = Version(
				algorithm=algorithm,
				description=description,
				number=version_number,
				source_code=source_code,
				publishing_state='En Desarrollo',
				created_by=current_user
			)
			new_algorithm_version.save()
			return HttpResponseRedirect(reverse('algorithm:detail', kwargs={'algorithm_id': algorithm_id}))
		else:
			version_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		version_form = VersionForm()
	context = {'version_form': version_form, 'algorithm': algorithm, 'new_major_version': new_major_version_number,
	           'new_minor_version': new_minor_version_number}
	return render(request, 'algorithm/new_version.html', context)


@login_required(login_url='/accounts/login/')
def update_version(request, algorithm_id, version_id):
	version = get_object_or_404(Version, id=version_id)
	if request.method == 'POST':
		# getting the form
		version_form = VersionUpdateForm(request.POST)
		# checking if the form is valid
		if version_form.is_valid():
			print 'formulario válido!'
			description = version_form.cleaned_data['description']
			source_code = version_form.cleaned_data['source_code']
			# updating with the new information
			version.description = description
			version.source_code = source_code
			version.save()
			return HttpResponseRedirect(reverse('algorithm:detail', kwargs={'algorithm_id': algorithm_id}))
		else:
			version_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		version_form = VersionUpdateForm(initial={'description': version.description,
		                                          'source_code': version.source_code})
	context = {'version_form': version_form, 'version': version}
	return render(request, 'algorithm/update_version.html', context)


@login_required(login_url='/accounts/login/')
def version_detail(request, algorithm_id, version_id):
	version = get_object_or_404(Version, id=version_id)
	parameters = Parameter.objects.filter(version=version_id).order_by('position')
	context = {'version': version, 'parameters': parameters}
	return render(request, 'algorithm/version_detail.html', context)


@login_required(login_url='/accounts/login/')
def publish_version(request, algorithm_id, version_id):
	version = get_object_or_404(Version, id=version_id)
	if request.method == 'GET':
		# TODO: What is the condition to be published?
		version.publishing_state = 'Publicada'
		version.save()
	return HttpResponseRedirect(
		reverse('algorithm:version_detail', kwargs={'algorithm_id': algorithm_id, 'version_id': version_id}))


@login_required(login_url='/accounts/login/')
def unpublish_version(request, algorithm_id, version_id):
	version = get_object_or_404(Version, id=version_id)
	if request.method == 'GET':
		if version.publishing_state == 'Publicada':
			version.publishing_state = 'En Desarrollo'
			version.save()
	return HttpResponseRedirect(
		reverse('algorithm:version_detail', kwargs={'algorithm_id': algorithm_id, 'version_id': version_id}))


@login_required(login_url='/accounts/login/')
def deprecate_version(request, algorithm_id, version_id):
	version = get_object_or_404(Version, id=version_id)
	if request.method == 'GET':
		if version.publishing_state == 'Publicada':
			version.publishing_state = 'Obsoleta'
			version.save()
	return HttpResponseRedirect(
		reverse('algorithm:version_detail', kwargs={'algorithm_id': algorithm_id, 'version_id': version_id}))


@login_required(login_url='/accounts/login/')
def delete_version(request, algorithm_id, version_id):
	version = get_object_or_404(Version, id=version_id)
	if request.method == 'GET':
		# TODO: This must validate if this version was already executed.
		# TODO: What happen if there is only one version?
		if version.algorithm.obtain_versions().count() > 1:
			version.delete()
	return HttpResponseRedirect(
		reverse('algorithm:detail', kwargs={'algorithm_id': algorithm_id}))


@login_required(login_url='/accounts/login/')
def new_parameter(request, algorithm_id, version_id):
	version = get_object_or_404(Version, id=version_id)
	if request.method == 'POST':
		# getting the form
		new_parameter_form = NewParameterForm(request.POST)
		# checking if the form is valid
		if new_parameter_form.is_valid():
			name = new_parameter_form.cleaned_data['name']
			parameter_type = new_parameter_form.cleaned_data['parameter_type']
			description = new_parameter_form.cleaned_data['description']
			help_text = new_parameter_form.cleaned_data['help_text']
			position = new_parameter_form.cleaned_data['position']
			required = new_parameter_form.cleaned_data['required']
			enabled = new_parameter_form.cleaned_data['enabled']
			default_value = new_parameter_form.cleaned_data['default_value']
			function_name = new_parameter_form.cleaned_data['function_name']
			# creating the parameter
			new_version_parameter = Parameter(
				version=version,
				name=name,
				parameter_type=parameter_type,
				description=description,
				help_text=help_text,
				position=position,
				required=required,
				enabled=enabled,
				default_value=default_value,
				function_name=function_name,
			)
			new_version_parameter.save()
			return HttpResponseRedirect(
				reverse('algorithm:version_detail', kwargs={'algorithm_id': algorithm_id, 'version_id': version_id}))
		else:
			new_parameter_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		new_parameter_form = NewParameterForm()
	context = {'new_parameter_form': new_parameter_form, 'version': version}
	return render(request, 'algorithm/new_parameter.html', context)


@login_required(login_url='/accounts/login/')
def view_parameter(request, algorithm_id, version_id, parameter_id):
	return render(request, 'algorithm/view_parameter.html')
