# -*- coding: utf-8 -*-

from django.contrib import admin
from algorithm.models import Algorithm
from algorithm.models import Topic
from algorithm.models import Version
from algorithm.models import Parameter
from algorithm.models import VersionStorageUnit


admin.site.register(Algorithm)
admin.site.register(Topic)
admin.site.register(Version)
admin.site.register(Parameter)
admin.site.register(VersionStorageUnit)
