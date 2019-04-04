# -*- coding: utf-8 -*-

from django.urls import path
from index.views import TaskIndexView

urlpatterns = [
    path('', TaskIndexView.as_view(), name='index'),
    # path('index/', IndexView.as_view(), name='index'),
]
