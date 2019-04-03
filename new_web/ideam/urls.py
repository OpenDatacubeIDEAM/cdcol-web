"""ideam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from algorithm.views import AlgorithmViewSet
from algorithm.views import VersionViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'algorithms', AlgorithmViewSet)
router.register(r'versions', VersionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),

    path('', include(('index.urls','index'))),

    path('accounts/',include('allauth.urls')),
    path('profile/', include(('user_profile.urls','profile'))),
    path('algorithm/', include(('algorithm.urls','algorithm'))),
    path('execution/', include(('execution.urls','execution'))),
    path('storage/', include(('storage.urls','storage'))),
]

if settings.DEBUG:
    # Serve media file during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files during development
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
