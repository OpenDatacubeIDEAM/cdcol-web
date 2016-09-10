from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from algorithm.models import Algorithm, Topic
from storage.models import StorageUnit
from algorithm.forms import AlgorithmForm

@login_required(login_url='/accounts/login/')
def index(request):
	current_user = request.user
	return render(request, 'algorithm/index.html')


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
			field_source_storage_unit = algorithm_form.cleaned_data['source_storage_unit']
			field_output_storage_unit = algorithm_form.cleaned_data['output_storage_unit']

			## TODO: Read the response and create the object

			# print field_topic
			# return render(request, 'algorithm/index.html')
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
