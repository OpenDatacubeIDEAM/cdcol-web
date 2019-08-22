# -*- coding: utf-8 -*-

from django.urls import path
from execution.views import ExecutionIndexView
from execution.views import ExecutionCreateView
from execution.views import AlgorithmsByTopicListView
from execution.views import VersionParametersJson
from execution.views import ExecutionDetailView
from execution.views import ExecutionRateView
from execution.views import ExecutionCancelView
from execution.views import DownloadResultImageView
from execution.views import DeleteResultImageView
from execution.views import GenerateGeoTiffTask
from execution.views import DownloadTaskLogView
from execution.views import ExecutionStateJsonView
from execution.views import ExecutionCopyView

urlpatterns = [
    path('', ExecutionIndexView.as_view(), name='index'),
    path('<int:pk>/detail',ExecutionDetailView.as_view(), name='detail'),
    path('<int:pk>/rate',ExecutionRateView.as_view(), name='rate'),
    path('<int:pk>/cancel',ExecutionCancelView.as_view(), name='cancel'),

    # This URL format can not be changed because the static/js/formBuilder.js 
    # require this forma in the URL to set the algoritm version in the 
    # select field.
    path('<int:epk>/version/<int:vpk>/copy', ExecutionCopyView.as_view(), name='copy'),

    path('<int:pk>/result/image/<str:image_name>/download',DownloadResultImageView.as_view(), name='image-download'),
    path('<int:pk>/result/image/<str:image_name>/delete',DeleteResultImageView.as_view(), name='image-delete'),
    path('<int:pk>/result/image/<str:image_name>/generate_geotiff_task',GenerateGeoTiffTask.as_view(), name='generate_geotiff_task'),

    path('state/json', ExecutionStateJsonView.as_view(), name='state-json'),

    path('task/log', DownloadTaskLogView.as_view(), name='task-download-log'),

    path('algorithm/list', AlgorithmsByTopicListView.as_view(), name='algorithm-list'),

    # This URL format can not be changed because the static/js/formBuilder.js 
    # require this forma in the URL to set the algoritm version in the 
    # select field.
    path('algorithm/version/<int:pk>', ExecutionCreateView.as_view(), name='create'),
    

    # This is used by formBuilder.js
    path('parameters/version/<int:pk>/json', VersionParametersJson.as_view(), name='version-parameters'),
]
