# -*- coding: utf-8 -*-

from django.contrib import admin
from template.models import Yaml
from template.models import Ingest


admin.site.register(Yaml)
admin.site.register(Ingest)
