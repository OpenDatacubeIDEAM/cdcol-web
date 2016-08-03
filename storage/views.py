from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	current_user = request.user
	return render(request, 'storage/index.html')
