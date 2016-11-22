from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
	return render(request, 'public/index.html')


@login_required(login_url='/accounts/login/')
def home(request):
	return render(request, 'public/home.html')
