from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from algorithm.models import Algorithm, Topic, AlgorithmStorageUnit
from storage.models import StorageUnit
from algorithm.forms import AlgorithmForm


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
			field_output_storage_unit = algorithm_form.cleaned_data['output_storage_unit']
			# creating the new algorithm
			new_algorithm = Algorithm(
				name=field_name,
				description=field_description,
				topic=field_topic,
				output_storage_unit=field_output_storage_unit,
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
			return HttpResponseRedirect(reverse('algorithm:index'))
		else:
			algorithm_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		algorithm_form = AlgorithmForm()
	context = {'algorithm_form': algorithm_form, 'topics': topics, 'source_storage_units': source_storage_units}
	return render(request, 'algorithm/new.html', context)


@login_required(login_url='/accounts/login/')
def detail(request, algorithm_id):
	return render(request, 'algorithm/detail.html')


@login_required(login_url='/accounts/login/')
def new_version(request, algorithm_id):
	return render(request, 'algorithm/new_version.html')


@login_required(login_url='/accounts/login/')
def version_detail(request, algorithm_id, version_id):
	return render(request, 'algorithm/version_detail.html')


@login_required(login_url='/accounts/login/')
def new_parameter(request, algorithm_id, version_id):
	return render(request, 'algorithm/new_parameter.html')


@login_required(login_url='/accounts/login/')
def view_parameter(request, algorithm_id, version_id, parameter_id):
	return render(request, 'algorithm/view_parameter.html')
