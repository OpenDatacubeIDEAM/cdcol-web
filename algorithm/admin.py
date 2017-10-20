from django.contrib import admin
from algorithm.models import *
from django.core.exceptions import PermissionDenied

class AlgorithmAdmin(admin.ModelAdmin):
        def save_model(self, request, obj, form, change):
                obj.user = request.user
                raise PermissionDenied

admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(Topic)
admin.site.register(VersionStorageUnit)
admin.site.register(Version, AlgorithmAdmin)
admin.site.register(Parameter, AlgorithmAdmin)
