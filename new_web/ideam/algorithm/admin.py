# -*- coding: utf-8 -*-

from django.contrib import admin
from algorithm.models import Algorithm
from algorithm.models import Topic


admin.site.register(Algorithm)
admin.site.register(Topic)