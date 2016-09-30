from django.conf.urls import url

from . import views

app_name = 'execution'
urlpatterns = [
	# ex: /execution/
	url(r'^$', views.index, name='index'),
	# ex: /execution/detail/11
	url(r'^detail/(?P<execution_id>[0-9]+)/$', views.detail, name='detail'),
	# ex: /execution/new
	url(r'^new/(?P<algorithm_id>[0-9]+)$', views.new, name='new'),
]