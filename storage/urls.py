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
	# ex: /storage/1/image/imagename/download/
	url(r'^download/image/(?P<storage_unit_name>.*)/(?P<image_name>.+)$', views.download_image, name='download_image'),
	# ex: /storage/1/image/imagename/metadata/
	url(r'^(?P<storage_unit_id>[0-9]+)/image/(?P<image_name>.+)/metadata/$', views.download_metadata, name='download_metadata'),
	# ex: /storage/1/[type]/download/
	url(r'^/download/file/(?P<storage_unit_name>.*)/(?P<file>.+)$', views.download_file, name='download_file'),
	# ex: /storage/storage_units/
	url(r'^storage_units/$', views.obtain_storage_units, name='obtain_storage_units'),
	# ex: /storage/content/12/json/
	url(r'^content/(?P<storage_unit_id>[0-9]+)/json/$', views.content_as_json, name='content_as_json'),
	# ex: /storage/content/12/
	url(r'^content/(?P<storage_unit_id>[0-9]+)/$', views.view_content, name='view_content'),
	# ex: /storage/1/image/12/detail/
	url(r'^(?P<storage_unit_id>[0-9]+)/image/(?P<image_name>.+)/detail/$', views.image_detail, name='image_detail'),
	# ex /storage/content_as_json
	url(r'^json$', views.as_json, name='as_json'),
	# ex: /storage/update/11
	url(r'^update/(?P<storage_unit_id>[0-9]+)/$', views.update, name='update'),
]
