# -*- coding: utf-8 -*-

from django.urls import path
from index.views import IndexView

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
    path('index/', IndexView.as_view(), name='index'),
]
