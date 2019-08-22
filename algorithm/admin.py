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

class VersionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'number',
        'publishing_state',
        'version_name',
        'algorithm_name',
        'algorithm_created_by'
    )

    def version_name(self,obj):
        return obj.name

    version_name.short_description = 'Nombre Version'

    def algorithm_name(self,obj):
        return obj.algorithm.name

    algorithm_name.short_description = 'Nombre Algorithmo'
    algorithm_name.admin_order_field = 'algorithm__name'

    def algorithm_created_by(self,obj):
        return obj.algorithm.created_by

    algorithm_created_by.short_description = 'Creado Por'
    algorithm_created_by.admin_order_field = 'algorithm__created_by'

    #def save_model(self, request, obj, form, change):
    #    obj.user = request.user
    #    raise PermissionDenied


admin.site.register(Topic)
admin.site.register(VersionStorageUnit)
admin.site.register(Algorithm,RestrictAdmin)
admin.site.register(Version,VersionAdmin)
admin.site.register(Parameter,RestrictAdmin)
