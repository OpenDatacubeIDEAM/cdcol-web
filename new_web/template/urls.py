# -*- coding: utf-8 -*-

from django.urls import path
from template.views import YamlIndexView

urlpatterns = [
    path('', YamlIndexView.as_view(), name='index'),
    # path('index/', IndexView.as_view(), name='index'),
]
