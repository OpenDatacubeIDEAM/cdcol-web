from django.conf.urls import url

from . import views

app_name = 'storage'
urlpatterns = [
	# ex: /storage/
	url(r'^$', views.index, name='index'),
	# ex: /storage/detail/11
	url(r'^detail/(?P<item_id>[0-9]+)/$', views.detail, name='detail'),
	# ex: /storage/ceos/new
	url(r'^ceos/new/$', views.new_ceos, name='new_ceos'),
	# ex: /storage/cdcol/new
	url(r'^cdcol/new/$', views.new_cdcol, name='new_cdcol'),
]