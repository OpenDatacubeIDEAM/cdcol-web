from django.contrib import admin
from ingest_template.models import *


class IngestTemplateAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'updated_at')
	admin.ModelAdmin.ordering = ('-created_at', )
	admin.ModelAdmin.list_per_page = 20

admin.site.register(IngestTemplate, IngestTemplateAdmin)
