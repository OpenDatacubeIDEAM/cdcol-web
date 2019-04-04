# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from ingest.serializers import TaskSerializer

from rest_framework import viewsets

from ingest.models import Task
from ingest.forms import TaskForm

class TaskIndexView(TemplateView):
    """Display a list of the algorithms."""
    template_name = 'ingest/index.html'


class TaskViewSet(viewsets.ModelViewSet):
    """CRUD over ingestion Task  model via API calls."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCreateView(CreateView):
    """Create an Ingestion Task.

    Use the template ingest/task_form.html
    """

    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('ingest:index')

    def form_valid(self, form):
        """
        Add the user to a task instance and initlilice the task
        state to Task.SCHEDULED_STATE

        This method is called when valid form data has been POSTed.
        """
        
        form.instance.created_by = self.request.user
        form.instance.state = Task.SCHEDULED_STATE
        self.object = form.save()
        return redirect(self.get_success_url())
 
    def get_context_data(self, **kwargs):
        """Add or change context initial data."""

        context = super(TaskCreateView, self).get_context_data(**kwargs)
        # Template aditional data
        context['section'] = 'Nueva Tarea de Ingesta'
        context['title'] = 'Nueva Tarea de Ingesta'
        context['button'] = 'Programar Tarea'
        return context


class TaskDetailView(DetailView):
    """Display Ingestion Task detail.

    Use the template ingest/task_detail.html
    """
    model = Task
    context_object_name = 'task'
