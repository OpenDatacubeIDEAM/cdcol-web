from django.conf.urls import url

from . import views

app_name = 'template'
urlpatterns = [
	# ex: /template/
	url(r'^$', views.index, name='index'),
	# ex: /template/download/filename.ext
	url(r'^download/(?P<template_id>.+)$', views.download_file, name='download_file'),
	# ex /template/json
	url(r'^json$', views.as_json, name='as_json'),
]
