# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import TemplateView


class PendingView(TemplateView):
    template_name = 'user_profile/pending.html'


class HomeView(TemplateView):
    template_name = 'user_profile/update.html'