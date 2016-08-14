from django.conf.urls import url

from . import views

app_name = 'algorithm'
urlpatterns = [
	# ex: /algorithm/
	url(r'^$', views.index, name='index'),
	# ex: /algorithm/new
	url(r'^new/$', views.new, name='new'),
]