from django.contrib import admin
from algorithm.models import *
from django.core.exceptions import PermissionDenied

class AlgorithmAdmin(admin.ModelAdmin):
        def save_model(self, request, obj, form, change):
                obj.user = request.user
                if not change:
                        super(ArticleAdmin, self).save_model(request, obj, form$
                else:
                        raise PermissionDenied

admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(Topic)
admin.site.register(VersionStorageUnit)
admin.site.register(Version, AlgorithmAdmin)
admin.site.register(Parameter, AlgorithmAdmin)
