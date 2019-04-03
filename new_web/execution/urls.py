# -*- coding: utf-8 -*-

from django.urls import path
from execution.views import ExecutionCreateView


urlpatterns = [
    path('execution/version/<int:pk>', ExecutionCreateView.as_view(), name='create'),
    # path('index/', IndexView.as_view(), name='index'),
]