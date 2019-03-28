 # -*- coding: utf-8 -*-

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
# from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView

from rest_framework import viewsets
from algorithm.models import Algorithm
from algorithm.models import Topic
from algorithm.serializers import AlgorithmSerializer
from algorithm.forms import AlgorithmForm


class AlgorithmIndexView(TemplateView):
	template_name = 'algorithm/index.html'


# ViewSets define the view behavior.
class AlgorithmViewSet(viewsets.ModelViewSet):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer


class AlgorithmCreateView(CreateView):

    model = Algorithm
    fields = ['name','description','topic']
    template_name = 'algorithm/create.html'
    success_url = reverse_lazy('algorithm:index')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.created_by = self.request.user
        return super().form_valid(form)
 
    def get_context_data(self, **kwargs):
        data = super(AlgorithmCreateView, self).get_context_data(**kwargs)
        topics = Topic.objects.filter(enabled=True)
        data['algorithm_form'] = data.get('form')
        data['topics'] = topics
        return data