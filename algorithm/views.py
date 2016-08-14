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

