from django.contrib import admin
from template.models import *


# class YamlAdmin(admin.ModelAdmin):
# 	list_display = ('name', 'type', 'created_at')
# 	# search_fields = ['name']
# 	admin.ModelAdmin.ordering = ('-created_at', )
# 	admin.ModelAdmin.list_per_page = 20
# 	# readonly_fields = ('id', 'type', 'name', 'file', 'updated_at')

# admin.site.register(YamlTemplate, YamlAdmin)
admin.site.register(YamlTemplate)
