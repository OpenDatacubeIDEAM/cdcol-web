# -*- coding: utf-8 -*-

from django.urls import path
from algorithm.views import AlgorithmIndexView
from algorithm.views import AlgorithmCreateView

urlpatterns = [
	path('create/', AlgorithmCreateView.as_view(), name='create'),
    path('index/', AlgorithmIndexView.as_view(), name='index'),
]
