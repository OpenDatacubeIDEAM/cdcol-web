from django.conf.urls import url

from . import views

app_name = 'profile'
urlpatterns = [
	# ex: /profile/
	url(r'^$', views.index, name='index'),
]