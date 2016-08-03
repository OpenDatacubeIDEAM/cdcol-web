from django.conf.urls import url

from . import views

app_name = 'storage'
urlpatterns = [
	# ex: /items/
	url(r'^$', views.index, name='index'),
]