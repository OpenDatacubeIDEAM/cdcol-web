# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from algorithm.models import Topic, Algorithm, Version


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
	return render(request, 'execution/new_blank_execution.html', context)


@login_required(login_url='/accounts/login/')
def new_execution(request, algorithm_id):
	current_user = request.user
	algorithm = get_object_or_404(Algorithm, id=algorithm_id)
	versions = Version.objects.filter(algorithm=algorithm).order_by('-number')
	topics = Topic.objects.all()
	context = {'topics': topics, 'algorithm': algorithm, 'versions': versions}
	return render(request, 'execution/new.html', context)
