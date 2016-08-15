from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def index(request):
	current_user = request.user
	return render(request, 'algorithm/index.html')


@login_required(login_url='/accounts/login/')
def new(request):
	current_user = request.user
	return render(request, 'algorithm/new.html')


@login_required(login_url='/accounts/login/')
def detail(request, algorithm_id):
	return render(request, 'algorithm/detail.html')


@login_required(login_url='/accounts/login/')
def new_version(request, algorithm_id):
	return render(request, 'algorithm/new_version.html')


@login_required(login_url='/accounts/login/')
def version_detail(request, algorithm_id, version_id):
	return render(request, 'algorithm/version_detail.html')