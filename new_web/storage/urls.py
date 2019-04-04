# -*- coding: utf-8 -*-

from django.urls import path
from storage.views import IndexView
from storage.views import StoragelistJsonView
from storage.views import StorageCreateView
from storage.views import StorageDetailView
from storage.views import StorageUpdateView
from storage.views import DownloadFileView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('json/', StoragelistJsonView.as_view(), name='as_json'),
    path('create/', StorageCreateView.as_view(), name='create'),
    path('<int:pk>/', StorageDetailView.as_view(), name='detail'),
	path('<int:pk>/update/', StorageUpdateView.as_view(), name='update'),
    path('<int:pk>/file/<str:file_name>/download/', DownloadFileView.as_view(), name='download-file'),
    # path('index/', IndexView.as_view(), name='index'),
]
