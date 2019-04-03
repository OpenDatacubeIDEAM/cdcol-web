# -*- coding: utf-8 -*-

from django.urls import path
from template.views import YamlIndexView
from template.views import IngestIndexView

urlpatterns = [
    path('yaml', YamlIndexView.as_view(), name='yaml-index'),
    path('ingest', IngestIndexView.as_view(), name='ingest-index'),
    # path('index/', IndexView.as_view(), name='index'),
]
