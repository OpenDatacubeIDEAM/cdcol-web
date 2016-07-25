from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	current_user = request.user
	if current_user.is_authenticated():
		message = "Hola {}".format(current_user.username)
	else:
		message = "Hola. No estas autenticado"
	return HttpResponse(message)
