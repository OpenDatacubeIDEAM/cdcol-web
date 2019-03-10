from django.conf.urls import url

from . import views

app_name = 'algorithm'
urlpatterns = [
	# ex: /algorithm/
	url(r'^$', views.index, name='index'),
	# ex /algorithm/json/
	url(r'^json/$', views.as_json, name='as_json'),
	# ex: /algorithm/new
	url(r'^new/$', views.new, name='new'),
	# ex: /algorithm/detail/11
	url(r'^(?P<algorithm_id>[0-9]+)/detail/$', views.detail, name='detail'),
	# ex: /algorithm/update/11
	url(r'^update/(?P<algorithm_id>[0-9]+)/$', views.update, name='update'),
	# ex: /algorithm/11/version/new
	url(r'^(?P<algorithm_id>[0-9]+)/version/new$', views.new_version, name='new_version'),
	# ex: /algorithm/11/version/12/update
	url(r'^update/(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/update/$', views.update_version, name='update_version'),
	# ex: /algorithm/11/version/12/publish
	url(r'^update/(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/publish/$', views.publish_version, name='publish_version'),
	# ex: /algorithm/11/version/12/unpublish
	url(r'^update/(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/unpublish/$', views.unpublish_version, name='unpublish_version'),
	# ex: /algorithm/11/version/12/deprecate
	url(r'^update/(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/deprecate/$', views.deprecate_version, name='deprecate_version'),
	# ex: /algorithm/11/version/12/delete
	url(r'^update/(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/delete/$', views.delete_version, name='delete_version'),
	# ex: /algorithm/11/version/12/review
	url(r'^update/(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/review/$', views.review_version, name='review_version'),
	# ex: /algorithm/11/version/12
	url(r'^(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)$', views.version_detail, name='version_detail'),
	# ex: /algorithm/11/version/12/download
	url(r'^version/download/sourcecode/(?P<source_code_route>.*)', views.download_version, name='download_version'),
	# ex: /algorithm/11/version/12/ratings
	url(r'^(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/ratings$', views.version_rating, name='version_rating'),
	# ==== Params ====
	# ex: /algorithm/11/version/12/param/new
	url(r'^(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/parameter/new$', views.new_parameter,
	    name='new_parameter'),
	# ex: /algorithm/11/version/12/param/12
	url(r'^(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/parameter/(?P<parameter_id>[0-9]+)$', views.view_parameter,
	    name='view_parameter'),
	# ex: /algorithm/11/version/12/param/13/update
	url(r'^(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/parameter/(?P<parameter_id>[0-9]+)/update/$', views.update_parameter, name='update_parameter'),
	# ex: /algorithm/versions
	url(r'^versions/$', views.version_review_list, name='version_review_list'),
]
