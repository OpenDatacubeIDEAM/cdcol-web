# -*- coding: utf-8 -*-

from django.urls import path
from storage.views import IndexView
from storage.views import StoragelistJsonView
from storage.views import StorageCreateView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('json/', StoragelistJsonView.as_view(), name='as_json'),
    path('create/', StorageCreateView.as_view(), name='create'),
    # path('index/', IndexView.as_view(), name='index'),
]
