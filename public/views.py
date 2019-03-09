from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def index(request):

	if request.user.is_superuser:
		# Super users does not have UserProfile
		# since they are created using the 
		# createsuper user command that creates 
		# User instances.
		return redirect('admin/')

	if request.user.is_authenticated():
		return render(request, 'public/home.html')

	return render(request, 'public/index.html')


@login_required(login_url='/accounts/login/')
def home(request):
	return render(request, 'public/home.html')
