# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from algorithm.models import Topic, Algorithm, Version, Parameter


@login_required(login_url='/accounts/login/')
def index(request):
	current_user = request.user
	return render(request, 'execution/index.html')


@login_required(login_url='/accounts/login/')
def detail(request, execution_id):
	return render(request, 'execution/detail.html')


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

	context = {'topics': topics, 'algorithm': algorithm, 'versions': versions, 'parameters': parameters}
	return render(request, 'execution/new.html', context)