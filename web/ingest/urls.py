from django.conf.urls import url

from . import views

app_name = 'ingest'
urlpatterns = [
	# ex: /ingest/
	url(r'^$', views.index, name='index'),
	# ex /ingest/json/
	url(r'^json/$', views.as_json, name='as_json'),
	# ex /ingest/new
	url(r'^new/$', views.new, name='new'),
	# ex /ingest/detail
	url(r'^detail/(?P<ingest_task_id>[0-9]+)/$', views.detail, name='detail'),
]