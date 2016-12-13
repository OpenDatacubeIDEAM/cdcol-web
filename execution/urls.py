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
	url(r'^(?P<execution_id>[0-9]+)/image/(?P<image_name>.+)/download/$', views.download_result, name='download_result'),
	# ex: /execution/new
	url(r'^new/$', views.new_blank_execution, name='new_blank_execution'),
	# # ex: /execution/new/12/version/11
	url(r'^new/(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/$', views.new_execution, name='new_execution'),
	# ex: /execution/parameters/11
	url(r'^parameters/(?P<version_id>[0-9]+)/$', views.obtain_parameters, name='obtain_parameters'),
	# # ex: /execution/12/rate
	url(r'^(?P<execution_id>[0-9]+)/rate/$', views.rate_execution, name='rate_execution'),
]