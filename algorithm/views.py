# -*- coding: utf-8 -*-
import os
import mimetypes
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Avg, Q
from algorithm.models import Algorithm, Topic, VersionStorageUnit, Version, Parameter
from algorithm.serializers import AlgorithmSerializer
from execution.models import Review
from storage.models import StorageUnit
from execution.models import Execution
from algorithm.forms import AlgorithmForm, AlgorithmUpdateForm, VersionForm, VersionUpdateForm, NewParameterForm
from rest_framework.renderers import JSONRenderer
from django.conf import settings
import urllib
from django.core.files import File
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str


class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""

	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


def is_data_admin(user):
	return user.groups.filter(name='DataAdmin').exists()


def as_json(request):
	current_user = request.user
	if is_data_admin(current_user):
		queryset = Algorithm.objects.filter()
	else:
		queryset = Algorithm.objects.filter(created_by=current_user)
	serializer = AlgorithmSerializer(queryset, many=True)
	return JSONResponse(serializer.data)


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_list_algorithms', raise_exception=True)
def index(request):
	return render(request, 'algorithm/index.html')


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_create_algorithm', raise_exception=True)
def new(request):
	current_user = request.user
	topics = Topic.objects.filter(enabled=True)
	if request.method == 'POST':
		# getting the form
		algorithm_form = AlgorithmForm(request.POST)
		# checking if the form is valid
		if algorithm_form.is_valid():
			field_topic = algorithm_form.cleaned_data['topic']
			field_name = algorithm_form.cleaned_data['name']
			field_display_name = algorithm_form.cleaned_data['display_name']
			field_description = algorithm_form.cleaned_data['description']
			# creating the new algorithm
			new_algorithm = Algorithm(
				name=field_name,
				display_name=field_display_name,
				description=field_description,
				topic=field_topic,
				created_by=current_user
			)
			new_algorithm.save()
			# creating the base version
			new_algorithm_version = Version(
				algorithm=new_algorithm,
				description='Versión por defecto 1.0',
				number='1.0',
				repository_url='',
				publishing_state=Version.DEVELOPED_STATE,
				created_by=current_user
			)
			new_algorithm_version.save()
			return HttpResponseRedirect(reverse('algorithm:index'))
		else:
			algorithm_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		algorithm_form = AlgorithmForm()
	context = {'algorithm_form': algorithm_form, 'topics': topics}
	return render(request, 'algorithm/new.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_edit_algorithm', raise_exception=True)
def update(request, algorithm_id):
	current_user = request.user
	algorithm = get_object_or_404(Algorithm, Q(created_by=current_user), id=algorithm_id)
	if request.method == 'POST':
		# getting the form
		algorithm_form = AlgorithmUpdateForm(request.POST)
		# checking if the form is valid
		if algorithm_form.is_valid():
			field_name = algorithm_form.cleaned_data['name']
			field_display_name = algorithm_form.cleaned_data['display_name']
			field_description = algorithm_form.cleaned_data['description']
			# update the algorithm
			algorithm.name = field_name
			algorithm.description = field_description
			algorithm.save()
			return HttpResponseRedirect(reverse('algorithm:detail', kwargs={'algorithm_id': algorithm_id}))
		else:
			algorithm_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		algorithm_form = AlgorithmUpdateForm()
	context = {'algorithm_form': algorithm_form, 'algorithm': algorithm}
	return render(request, 'algorithm/update.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_view_algorithm_detail', raise_exception=True)
def detail(request, algorithm_id):
	current_user = request.user
	if is_data_admin(current_user):
		algorithm = get_object_or_404(Algorithm, id=algorithm_id)
	else:
		algorithm = get_object_or_404(Algorithm, Q(created_by=current_user), id=algorithm_id)
	versions = Version.objects.filter(algorithm_id=algorithm_id)
	context = {'algorithm': algorithm, 'versions': versions}
	return render(request, 'algorithm/detail.html', context)


def download_source_code(new_version):
	# deleting the old file if there is any
	try:
		os.remove("{}/{}".format(settings.MEDIA_ROOT, new_version.source_code.name))
	except:
		pass
	try:
		# getting the file name
		file_name = new_version.repository_url.split('/')[-1]
		# downloading and updating the model
		content = urllib.urlretrieve(new_version.repository_url)
		new_version.source_code.save(file_name, File(open(content[0])), save=True)
	except:
		print "Something went wrong when downloading, {}".format(new_version.repository_url)
		pass



@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_create_new_version', raise_exception=True)
def new_version(request, algorithm_id):
	current_user = request.user
	algorithm = get_object_or_404(Algorithm, Q(created_by=current_user), id=algorithm_id)
	current_version = algorithm.last_version()
	try:
		new_minor_version_number = current_version.new_minor_version()
		new_major_version_number = current_version.new_major_version()
	except:
		new_minor_version_number = "1.0"
		new_major_version_number = "1.0"
	source_storage_units = StorageUnit.objects.all()
	if request.method == 'POST':
		# getting the form
		version_form = VersionForm(request.POST)
		# checking if the form is valid
		if version_form.is_valid():
			description = version_form.cleaned_data['description']
			version_number = version_form.cleaned_data['number']
			repository_url = version_form.cleaned_data['repository_url']
			field_source_storage_units = version_form.cleaned_data['source_storage_units']
			# reading the version
			version_number = new_minor_version_number if version_number == "1" else new_major_version_number
			# creating the new version
			new_algorithm_version = Version(
				algorithm=algorithm,
				description=description,
				number=version_number,
				repository_url=repository_url,
				publishing_state=Version.DEVELOPED_STATE,
				created_by=current_user
			)
			new_algorithm_version.save()
			download_source_code(new_algorithm_version)
			# creating the relation with the storage units
			for source_storage_unit in field_source_storage_units:
				new_version_relation = VersionStorageUnit(
					version=new_algorithm_version,
					storage_unit=source_storage_unit
				)
				new_version_relation.save()
			return HttpResponseRedirect(reverse('algorithm:detail', kwargs={'algorithm_id': algorithm_id}))
		else:
			version_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		version_form = VersionForm()
	context = {'version_form': version_form, 'algorithm': algorithm, 'new_major_version': new_major_version_number,
	           'new_minor_version': new_minor_version_number, 'source_storage_units': source_storage_units}
	return render(request, 'algorithm/new_version.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_edit_version', raise_exception=True)
def update_version(request, algorithm_id, version_id):
	current_user = request.user
	version = get_object_or_404(Version, Q(created_by=current_user), id=version_id)
	selected_storage_units = version.source_storage_units.all()
	source_storage_units = StorageUnit.objects.all()
	if request.method == 'POST':
		# getting the form
		version_form = VersionUpdateForm(request.POST)
		if version.publishing_state != Version.DEVELOPED_STATE:
			version_form.add_error(None, "Solo es posible actualizar una versión si esta se encuentra en estado 'En Desarrollo'.")
		# checking if the form is valid
		if version_form.is_valid():
			description = version_form.cleaned_data['description']
			repository_url = version_form.cleaned_data['repository_url']
			field_source_storage_units = version_form.cleaned_data['source_storage_units']
			# updating with the new information
			version.description = description
			version.repository_url = repository_url
			version.save()
			# downloading the new file
			download_source_code(version)
			# deleting all the source storage units associations
			version_associations = VersionStorageUnit.objects.filter(version_id=version.id)
			for association in version_associations:
				association.delete()
			# creating all the new associations
			for source_storage_unit in field_source_storage_units:
				new_version_relation = VersionStorageUnit(
					version=version,
					storage_unit=source_storage_unit
				)
				new_version_relation.save()
			return HttpResponseRedirect(reverse('algorithm:version_detail', kwargs={'algorithm_id': algorithm_id, 'version_id': version.id }))
		else:
			version_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		version_form = VersionUpdateForm(initial={'description': version.description,
		                                          'repository_url': version.repository_url})
	context = {'version_form': version_form, 'version': version, 'selected_storage_units': selected_storage_units,
	           'source_storage_units': source_storage_units}
	return render(request, 'algorithm/update_version.html', context)


@login_required(login_url='/accounts/login/')
def download_version(request, algorithm_id, version_id):
	"""
	Download a file using the version_id
	"""
	version = get_object_or_404(Version, id=version_id)
	file_name = version.repository_url.split('/')[-1]
	file_path = "{}/{}".format(settings.MEDIA_ROOT, version.source_code.name)
	file_wrapper = FileWrapper(file(file_path, 'rb'))
	file_mimetype = mimetypes.guess_type(file_path)
	response = HttpResponse(file_wrapper, content_type=file_mimetype)
	response['X-Sendfile'] = file_path
	response['Content-Length'] = os.stat(file_path).st_size
	response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
	return response


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_view_version_detail', raise_exception=True)
def version_detail(request, algorithm_id, version_id):
	current_user = request.user
	if is_data_admin(current_user):
		version = get_object_or_404(Version, id=version_id)
	else:
		version = get_object_or_404(Version, Q(created_by=current_user), id=version_id)
	parameters = Parameter.objects.filter(version=version_id).order_by('position')
	reviews = Review.objects.filter(execution__version=version).order_by('created_at')
	# getting version executions
	execution_count = Execution.objects.filter(version=version).count()
	# getting the average rating
	average_rating = Review.objects.filter(version=version).aggregate(Avg('rating'))['rating__avg']
	average_rating = average_rating if average_rating is not None else 0
	storage_units = VersionStorageUnit.objects.filter(version_id=version_id)
	context = {'version': version, 'storage_units': storage_units, 'parameters': parameters, 'reviews': reviews,
	           'average_rating': average_rating, 'execution_count': execution_count}
	return render(request, 'algorithm/version_detail.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_view_ratings', raise_exception=True)
def version_rating(request, algorithm_id, version_id):
	version = get_object_or_404(Version, id=version_id)
	parameters = Parameter.objects.filter(version=version_id).order_by('position')
	reviews = Review.objects.filter(execution__version=version).order_by('created_at')
	# getting the average rating
	average_rating = Review.objects.filter(version=version).aggregate(Avg('rating'))['rating__avg']
	average_rating = round(average_rating if average_rating is not None else 0, 2)
	storage_units = VersionStorageUnit.objects.filter(version_id=version_id)
	context = {'version': version, 'storage_units': storage_units, 'parameters': parameters, 'reviews': reviews,
	           'average_rating': average_rating}
	return render(request, 'algorithm/version_rating.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_publish_version', raise_exception=True)
def publish_version(request, algorithm_id, version_id):
	current_user = request.user
	if is_data_admin(current_user):
		version = get_object_or_404(Version, id=version_id)
	else:
		version = get_object_or_404(Version, Q(created_by=current_user), id=version_id)
	if request.method == 'GET':
		if version.publishing_state == Version.DEVELOPED_STATE:
			version.publishing_state = Version.PUBLISHED_STATE
			version.save()
		else:
			print "Trying to publish a version, state is not 'in develop'"
	return HttpResponseRedirect(
		reverse('algorithm:version_detail', kwargs={'algorithm_id': algorithm_id, 'version_id': version_id}))


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_unpublish_version', raise_exception=True)
def unpublish_version(request, algorithm_id, version_id):
	current_user = request.user
	if is_data_admin(current_user):
		version = get_object_or_404(Version, id=version_id)
	else:
		version = get_object_or_404(Version, Q(created_by=current_user), id=version_id)
	if request.method == 'GET':
		execution_count = Execution.objects.filter(version=version).count()
		if version.publishing_state == Version.PUBLISHED_STATE and execution_count == 0:
			version.publishing_state = Version.DEVELOPED_STATE
			version.save()
		else:
			print "Trying to unpublish a version, state is not published or executions are not 0"
	return HttpResponseRedirect(
		reverse('algorithm:version_detail', kwargs={'algorithm_id': algorithm_id, 'version_id': version_id}))


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_deprecate_version', raise_exception=True)
def deprecate_version(request, algorithm_id, version_id):
	current_user = request.user
	if is_data_admin(current_user):
		version = get_object_or_404(Version, id=version_id)
	else:
		version = get_object_or_404(Version, Q(created_by=current_user), id=version_id)
	if request.method == 'GET':
		if version.publishing_state == Version.PUBLISHED_STATE:
			version.publishing_state = Version.DEPRECATED_STATE
			version.save()
		else:
			print "Trying to deprecate version, state is not published"
	return HttpResponseRedirect(
		reverse('algorithm:version_detail', kwargs={'algorithm_id': algorithm_id, 'version_id': version_id}))


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_delete_version', raise_exception=True)
def delete_version(request, algorithm_id, version_id):
	current_user = request.user
	if is_data_admin(current_user):
		version = get_object_or_404(Version, id=version_id)
	else:
		version = get_object_or_404(Version, Q(created_by=current_user), id=version_id)
	version = get_object_or_404(Version, id=version_id)
	if request.method == 'GET':
		execution_count = Execution.objects.filter(version=version).count()
		# if execution_count == 0 and version.algorithm.obtain_versions().count() > 1: # TODO: Must ask this
		if execution_count == 0:
			version.delete()
		else:
			print "Trying to delete version but there are executions"
	return HttpResponseRedirect(
		reverse('algorithm:detail', kwargs={'algorithm_id': algorithm_id}))


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_create_parameter', raise_exception=True)
def new_parameter(request, algorithm_id, version_id):
	current_user = request.user
	version = get_object_or_404(Version, Q(created_by=current_user), id=version_id)
	if request.method == 'POST':
		# getting the form
		new_parameter_form = NewParameterForm(request.POST)
		if version.publishing_state != Version.DEVELOPED_STATE:
			new_parameter_form.add_error(None, "Solo es posible agregar parámetros a versiones en estado 'En Desarrollo'.")
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
			output_included = new_parameter_form.cleaned_data['output_included']
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
				output_included=output_included,
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
@permission_required('algorithm.can_view_parameter_detail', raise_exception=True)
def view_parameter(request, algorithm_id, version_id, parameter_id):
	current_user = request.user
	if is_data_admin(current_user):
		parameter = get_object_or_404(Parameter, id=parameter_id)
	else:
		version = get_object_or_404(Version, Q(created_by=current_user), id=version_id)
		parameter = get_object_or_404(Parameter, id=parameter_id)
	context = {'parameter': parameter}
	return render(request, 'algorithm/parameter_detail.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('algorithm.can_edit_parameter', raise_exception=True)
def update_parameter(request, algorithm_id, version_id, parameter_id):
	current_user = request.user
	parameter = get_object_or_404(Parameter, id=parameter_id)
	version = get_object_or_404(Version, Q(created_by=current_user), id=version_id)
	if request.method == 'POST':
		# getting the form
		parameter_form = NewParameterForm(request.POST)
		if parameter.version.publishing_state != Version.DEVELOPED_STATE:
			parameter_form.add_error(None, "Solo es posible actualizar parámetros a versiones en estado 'En Desarrollo'.")
		# checking if the form is valid
		if parameter_form.is_valid():
			name = parameter_form.cleaned_data['name']
			parameter_type = parameter_form.cleaned_data['parameter_type']
			description = parameter_form.cleaned_data['description']
			help_text = parameter_form.cleaned_data['help_text']
			position = parameter_form.cleaned_data['position']
			required = parameter_form.cleaned_data['required']
			enabled = parameter_form.cleaned_data['enabled']
			default_value = parameter_form.cleaned_data['default_value']
			function_name = parameter_form.cleaned_data['function_name']
			output_included = parameter_form.cleaned_data['output_included']
			# updating the model
			parameter.name = name
			parameter.parameter_type = parameter_type
			parameter.description = description
			parameter.help_text = help_text
			parameter.position = position
			parameter.required = required
			parameter.enabled = enabled
			parameter.default_value = default_value
			parameter.function_name = function_name
			parameter.output_included = output_included
			parameter.save()
			return HttpResponseRedirect(reverse('algorithm:view_parameter', kwargs={'algorithm_id': algorithm_id, 'version_id': version_id, 'parameter_id': parameter_id}))
		else:
			parameter_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		parameter_form = NewParameterForm(initial={'name': parameter.name,
		                                           'parameter_type': parameter.parameter_type,
		                                           'description': parameter.description,
		                                           'help_text': parameter.help_text,
		                                           'position': parameter.position,
		                                           'required': parameter.required,
		                                           'enabled': parameter.enabled,
		                                           'default_value': parameter.default_value,
		                                           'function_name': parameter.function_name,
		                                           'output_included': parameter.output_included,})
	context = {'parameter_form': parameter_form, 'parameter': parameter}
	return render(request, 'algorithm/update_parameter.html', context)
