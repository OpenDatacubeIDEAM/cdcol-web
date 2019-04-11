# -*- coding: utf-8 -*-

from django.urls import path
from execution.views import ExecutionIndexView
from execution.views import ExecutionCreateView
from execution.views import AlgorithmsByTopicListView
from execution.views import VersionParametersJson
from execution.views import ExecutionDetailView
from execution.views import DeleteResultView
from execution.views import ExecutionRateView
from execution.views import ExecutionCopyView


urlpatterns = [
    path('', ExecutionIndexView.as_view(), name='index'),
    path('<int:pk>/detail',ExecutionDetailView.as_view(), name='detail'),
    path('<int:pk>/rate/',ExecutionRateView.as_view(), name='rate'),
    path('<int:pk>/copy/',ExecutionCopyView.as_view(), name='copy'),
    path('<int:pk>/result/image/<str:image_name>',DeleteResultView.as_view(), name='result-delete'),

    path('algorithm/list', AlgorithmsByTopicListView.as_view(), name='algorithm-list'),
    path('algorithm/version/<int:pk>', ExecutionCreateView.as_view(), name='create'),

    # This is used by formBuilder.js
    path('parameters/version/<int:pk>/json', VersionParametersJson.as_view(), name='version-parameters'),
]

# # ex: /execution/detail/11
# url(r'^(?P<execution_id>[0-9]+)/detail/$', views.detail, name='detail'),
# # ex: /execution/11/image/[image_name.nc]/download/
# url(r'^download/image/(?P<execution_id>[0-9]+)/(?P<image_name>.+)$', views.download_result, name='download_result'),
# # ex: /execution/11/image/[image_name.nc]/delete/
# url(r'^(?P<execution_id>[0-9]+)/image/(?P<image_name>.+)/delete/$', views.delete_result, name='delete_result'),
# # ex: /execution/11/zip/[parameter_name]/[file_name]/download/
# url(r'^download/zip/(?P<execution_id>[0-9]+)/(?P<parameter_name>.+)/(?P<file_name>.+)$', views.download_parameter_file, name='download_parameter_file'),
# # ex: /execution/11/image/[image_name.nc]/geotiff/
# url(r'^(?P<execution_id>[0-9]+)/image/(?P<image_name>.+)/geotiff/$', views.generate_geotiff, name='generate_geotiff'),
# url(r'^generate_geotiff/(?P<execution_id>[0-9]+)/(?P<image_name>.+)$', views.generate_geotiff_task, name='generate_geotiff_task'),
# # # ex: /execution/new/12/version/11
# url(r'^new/(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/$', views.new_execution, name='new_execution'),
# # # ex: /execution/new/12/version/11/id/2
# url(r'^new/(?P<algorithm_id>[0-9]+)/version/(?P<version_id>[0-9]+)/id/(?P<copy_execution_id>[0-9]+)$', views.new_execution, name='new_copied_execution'),
# # ex: /execution/parameters/11
# url(r'^parameters/(?P<version_id>[0-9]+)/$', views.obtain_parameters, name='obtain_parameters'),
# # ex: /execution/12/rate
# url(r'^(?P<execution_id>[0-9]+)/rate/$', views.rate_execution, name='rate_execution'),
# # ex: /execution/cancel/12
# url(r'^(?P<execution_id>[0-9]+)/cancel/$', views.cancel_execution, name='cancel_execution'),