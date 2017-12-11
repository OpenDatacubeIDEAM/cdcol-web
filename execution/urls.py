from django.conf.urls import url

from . import views

app_name = 'execution'
urlpatterns = [
	# ex: /execution/
	url(r'^$', views.index, name='index'),
	# ex /execution/json/
	url(r'^json/$', views.as_json, name='as_json'),
	# ex: /execution/detail/11
	url(r'^(?P<execution_id>[0-9]+)/detail/$', views.detail, name='detail'),
	# ex: /execution/11/image/[image_name.nc]/download/
	url(r'^download/image/(?P<execution_id>[0-9]+)/(?P<image_name>.+)$', views.download_result, name='download_result'),
	# ex: /execution/11/image/[image_name.nc]/delete/
	url(r'^(?P<execution_id>[0-9]+)/image/(?P<image_name>.+)/delete/$', views.delete_result, name='delete_result'),
	# ex: /execution/11/zip/[parameter_name]/[file_name]/download/
	url(r'^download/zip/(?P<execution_id>[0-9]+)/(?P<parameter_name>.+)/(?P<file_name>.+)$', views.download_parameter_file, name='download_parameter_file'),
	# ex: /execution/11/image/[image_name.nc]/geotiff/
	url(r'^(?P<execution_id>[0-9]+)/image/(?P<image_name>.+)/geotiff/$', views.generate_geotiff, name='generate_geotiff'),
	# ex: /execution/new
	url(r'^new/$', views.new_blank_execution, name='new_blank_execution'),
	# # ex: /execution/new/12/version/11
	url(r'^new/(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/$', views.new_execution, name='new_execution'),
	# # ex: /execution/new/12/version/11/id/2
	url(r'^new/(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/id/(?P<copy_execution_id>[0-9]+)$', views.new_execution, name='new_copied_execution'),
	# ex: /execution/parameters/11
	url(r'^parameters/(?P<version_id>[0-9]+)/$', views.obtain_parameters, name='obtain_parameters'),
	# # ex: /execution/12/rate
	url(r'^(?P<execution_id>[0-9]+)/rate/$', views.rate_execution, name='rate_execution'),
]
