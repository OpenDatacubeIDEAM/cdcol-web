# -*- coding: utf-8 -*-

from django.urls import path
from ingest.views import TaskIndexView
from ingest.views import TaskCreateView
from ingest.views import TaskDetailView

urlpatterns = [
    path('', TaskIndexView.as_view(), name='index'),
    path('task/create/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
