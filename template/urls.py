from django.conf.urls import url

from . import views

app_name = 'template'
urlpatterns = [
	# ex: /template/
	url(r'^$', views.index, name='index'),
]