# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required

from rest_framework import viewsets

from template.serializers import YamlSerializer
from template.serializers import IngestSerializer
from template.models import Yaml
from template.models import Ingest


@method_decorator(
    permission_required(
        'template.can_list_yaml_templates',
        raise_exception=True
    ),
    name='dispatch'
)
class YamlIndexView(LoginRequiredMixin,TemplateView):
    """Display the Yaml template list."""
    template_name = 'template/yaml_template_index.html'


class YamlViewSet(viewsets.ModelViewSet):
    """CRUD over Yaml model via API calls."""
    queryset = Yaml.objects.all()
    serializer_class = YamlSerializer


@method_decorator(
    permission_required(
        'template.can_list_ingest_templates',
        raise_exception=True
    ),
    name='dispatch'
)
class IngestIndexView(LoginRequiredMixin,TemplateView):
    """Display the ingest template list."""
    template_name = 'template/ingest_template_index.html'


class IngestViewSet(viewsets.ModelViewSet):
    """CRUD over ingest model via API calls."""
    queryset = Ingest.objects.all()
    serializer_class = IngestSerializer