# -*- coding: utf-8 -*-

from django.contrib import admin
from algorithm.models import Algorithm
from algorithm.models import Topic
from algorithm.models import Version
from algorithm.models import Parameter
from algorithm.models import VersionStorageUnit
from django.core.exceptions import PermissionDenied


class RestrictAdmin(admin.ModelAdmin):
        def save_model(self, request, obj, form, change):
                obj.user = request.user
                raise PermissionDenied


admin.site.register(Topic)
admin.site.register(VersionStorageUnit)
admin.site.register(Algorithm,RestrictAdmin)
admin.site.register(Version,RestrictAdmin)
admin.site.register(Parameter,RestrictAdmin)
