from django.conf.urls import url

from . import views

app_name = 'template'
urlpatterns = [
	# ex: /template/
	url(r'^$', views.index, name='index'),
	# ex: /template/download/filename.ext
	url(r'^download/(?P<full_file_name>.+)$', views.download_file, name='download_file'),
]