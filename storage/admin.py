# -*- coding: utf-8 -*-

from django.contrib import admin
from storage.models import StorageUnit
from django.core.exceptions import PermissionDenied


class StorageUnitAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        raise PermissionDenied

admin.site.register(StorageUnit, StorageUnitAdmin)