from django.conf.urls import url

from . import views

app_name = 'algorithm'
urlpatterns = [
	# ex: /algorithm/
	url(r'^$', views.index, name='index'),
	# ex: /algorithm/new
	url(r'^new/$', views.new, name='new'),
	# ex: /algorithm/detail/11
	url(r'^detail/(?P<algorithm_id>[0-9]+)/$', views.detail, name='detail'),
	# ex: /algorithm/update/11
	url(r'^update/(?P<algorithm_id>[0-9]+)/$', views.update, name='update'),
	# ex: /algorithm/11/version/new
	url(r'^(?P<algorithm_id>[0-9]+)/version/new$', views.new_version, name='new_version'),
	# ex: /algorithm/11/version/12
	url(r'^(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)$', views.version_detail, name='version_detail'),
	# ex: /algorithm/11/version/12/param/new
	url(r'^(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/parameter/new$', views.new_parameter,
	    name='new_parameter'),
	# ex: /algorithm/11/version/12/param/12
	url(r'^(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/parameter/(?P<parameter_id>[0-9]+)$', views.view_parameter,
	    name='view_parameter'),

]