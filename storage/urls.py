from django.conf.urls import url

from . import views

app_name = 'storage'
urlpatterns = [
	# ex: /storage/
	url(r'^$', views.index, name='index'),
	# ex: /storage/detail/11
	url(r'^detail/(?P<storage_unit_id>[0-9]+)/$', views.detail, name='detail'),
	# ex: /storage/new
	url(r'^new/$', views.new, name='new'),
	# ex: /storage/download/filename.ext
	url(r'^download/(?P<file_name>.+)$', views.download_file, name='download_file'),
	# ex: /storage/storage_units/
	url(r'^storage_units/$', views.obtain_storage_units, name='obtain_storage_units'),
	# ex: /storage/content/12/path=/
	url(r'^content/(?P<storage_unit_id>[0-9]+)/path=(?P<path>.+)*$', views.view_content, name='view_content'),
]