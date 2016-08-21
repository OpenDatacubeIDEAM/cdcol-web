from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def index(request):
	current_user = request.user
	return render(request, 'execution/index.html')


@login_required(login_url='/accounts/login/')
def detail(request, execution_id):
	return render(request, 'execution/detail.html')