 # -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from rest_framework import viewsets
from algorithm.models import Algorithm
from algorithm.models import Topic
from algorithm.models import Version
from algorithm.serializers import AlgorithmSerializer


class AlgorithmIndexView(TemplateView):
    template_name = 'algorithm/index.html'


# ViewSets define the view behavior.
class AlgorithmViewSet(viewsets.ModelViewSet):
    queryset = Algorithm.objects.all()
    serializer_class = AlgorithmSerializer

    def get_queryset(self):
        """Filter the queryset depending of the user.
        
        DataAdmin can list all algorithms. Other users 
        can list only the algorithms they have created.
        """

        user = self.request.user
        if hasattr(user,'profile') and user.profile.is_data_admin():
            return super().get_queryset()

        return user.algorithm_set.all()
        

class AlgorithmCreateView(CreateView):

    model = Algorithm
    fields = ['name','description','topic']
    template_name = 'algorithm/create.html'
    success_url = reverse_lazy('algorithm:index')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.created_by = self.request.user
        self.object = form.save()

        # Creating new algorithm version 
        version = Version(
            algorithm=self.object ,
            description='Versión por defecto 1.0',
            number='1.0',
            repository_url='',
            publishing_state=Version.DEVELOPED_STATE,
            created_by=self.request.user
        )
        version.save()
        return redirect(self.get_success_url())
 
    def get_context_data(self, **kwargs):
        data = super(AlgorithmCreateView, self).get_context_data(**kwargs)
        topics = Topic.objects.filter(enabled=True)
        data['algorithm_form'] = data.get('form')
        data['topics'] = topics
        return data
