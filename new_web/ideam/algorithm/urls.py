# -*- coding: utf-8 -*-

from django.urls import path
from algorithm.views import AlgorithmIndexView
from algorithm.views import AlgorithmCreateView
from algorithm.views import AlgorithmDetailView
from algorithm.views import VersionDetailView
from algorithm.views import VersionUpdateView

urlpatterns = [
	path('', AlgorithmIndexView.as_view(), name='index'),
	path('create/', AlgorithmCreateView.as_view(), name='create'),
    path('<int:pk>/', AlgorithmDetailView.as_view(), name='detail'),
    path('version/<int:pk>/', VersionDetailView.as_view(), name='version-detail'),
    path('version/<int:pk>/', VersionUpdateView.as_view(), name='version-update'),
    path('version/<int:pk>/', VersionUpdateView.as_view(), name='version-download'),
]
