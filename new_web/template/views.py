# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView
from django.shortcuts import render
from rest_framework import viewsets

from template.serializers import YamlSerializer
from template.models import Yaml


class YamlIndexView(TemplateView):
    """Display the Yaml template list."""
    template_name = 'template/yaml_template_index.html'


class YamlViewSet(viewsets.ModelViewSet):
    """CRUD over Yaml model via API calls."""
    queryset = Yaml.objects.all()
    serializer_class = YamlSerializer
