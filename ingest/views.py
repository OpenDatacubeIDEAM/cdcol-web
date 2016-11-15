# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from ingest.models import IngestTask
from rest_framework.renderers import JSONRenderer
from ingest.serializers import IngestTaskSerializer
from django.core.urlresolvers import reverse
from ingest.forms import IngestTaskForm
from storage.models import StorageUnit


class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""

	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


def as_json(request):
	queryset = IngestTask.objects.all()
	serializer = IngestTaskSerializer(queryset, many=True)
	return JSONResponse(serializer.data)


@login_required(login_url='/accounts/login/')
def index(request):
	ingest_task = IngestTask.objects.all()
	context = {'ingest_task': ingest_task}
	return render(request, 'ingest/index.html', context)


@login_required(login_url='/accounts/login/')
def new(request):
	response = None
	# obtaining the current user
	current_user = request.user
	if request.method == 'POST':
		# getting the form
		ingest_form = IngestTaskForm(request.POST)
		# checking if the form is valid
		if ingest_form.is_valid():
			# getting all the fields
			storage_unit_id = ingest_form.cleaned_data['storage_unit']
			comments = ingest_form.cleaned_data['comments']
			state = IngestTask.SCHEDULED_STATE

			# getting the StorageUnit object
			storage_unit = get_object_or_404(StorageUnit, id=storage_unit_id)

			# # creating the generic model
			new_ingest_task = IngestTask(
				storage_unit=storage_unit,
				comments=comments,
				state=state,
				created_by=current_user
			)
			new_ingest_task.save()
			return HttpResponseRedirect(reverse('ingest:index'))
		else:
			ingest_form.add_error(None, "Favor completar todos los campos marcados.")
	else:
		ingest_form = IngestTaskForm()
	context = {'ingest_form': ingest_form, 'response': response}
	return render(request, 'ingest/new.html', context)


@login_required(login_url='/accounts/login/')
def detail(request, ingest_task_id):
	ingest_task = get_object_or_404(IngestTask, id=ingest_task_id)
	context = {'ingest_task': ingest_task}
	return render(request, 'ingest/detail.html', context)
