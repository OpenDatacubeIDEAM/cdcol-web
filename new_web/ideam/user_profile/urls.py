# -*- coding: utf-8 -*-

from django.urls import path
from user_profile.views import PendingView
from user_profile.views import HomeView

urlpatterns = [
	path('home/', HomeView.as_view(), name='home'),
    path('pending/', PendingView.as_view(), name='pending'),
]
