from django.shortcuts import render

from rest_framework import viewsets
from ingest.serializers import TaskSerializer
from ingest.models import Task


class TaskIndexView(TemplateView):
    """Display a list of the algorithms."""
    template_name = 'ingest/index.html'


class TaskViewSet(viewsets.ModelViewSet):
    """CRUD over ingestion Task  model via API calls."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


