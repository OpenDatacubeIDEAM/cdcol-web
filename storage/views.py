from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	current_user = request.user
	return render(request, 'storage/index.html')


def detail(request, item_id):
	print item_id
	current_user = request.user
	return render(request, 'storage/detail.html')


def new_ceos(request):
	current_user = request.user
	return render(request, 'storage/new_ceos.html')


def new_cdcol(request):
	current_user = request.user
	return render(request, 'storage/new_cdcol.html')