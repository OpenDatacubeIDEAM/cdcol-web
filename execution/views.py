from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from algorithm.models import Topic


@login_required(login_url='/accounts/login/')
def index(request):
	current_user = request.user
	return render(request, 'execution/index.html')


@login_required(login_url='/accounts/login/')
def detail(request, execution_id):
	return render(request, 'execution/detail.html')


@login_required(login_url='/accounts/login/')
def new(request):
	current_user = request.user
	topics = Topic.objects.all()
	context = {'topics': topics}
	return render(request, 'execution/new.html', context)
