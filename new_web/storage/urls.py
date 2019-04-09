# -*- coding: utf-8 -*-

from django.urls import path
from storage.views import IndexView
from storage.views import StoragelistJsonView
from storage.views import StorageCreateView
from storage.views import StorageDetailView
from storage.views import StorageUpdateView
from storage.views import DownloadFileView
from storage.views import StorageViewContentView
from storage.views import StorageViewContentJsonView
from storage.views import StorageImageDetailView
from storage.views import StorageDownloadImageView
from storage.views import StorageDownloadImageMetadataJsonView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('json/', StoragelistJsonView.as_view(), name='as_json'),
    path('create/', StorageCreateView.as_view(), name='create'),
    path('<int:pk>/', StorageDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', StorageUpdateView.as_view(), name='update'),
    path('<int:pk>/content/', StorageViewContentView.as_view(), name='content'),
    path('<int:pk>/content/json/', StorageViewContentJsonView.as_view(), name='content-json'),
    path('<int:pk>/file/<str:file_name>/download/', DownloadFileView.as_view(), name='download-file'),
    path('<int:pk>/image/<str:name>/detail/', StorageImageDetailView.as_view(), name='image-detail'),
    path('<int:pk>/image/<str:image_name>/download/', StorageDownloadImageView.as_view(), name='image-download'),
    path('<int:pk>/image/<str:name>/metadata/', StorageDownloadImageMetadataJsonView.as_view(), name='metadata-download'),
    
    # path('index/', IndexView.as_view(), name='index'),
]
