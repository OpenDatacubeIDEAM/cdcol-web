 # -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

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
    """Create an algorithm and an initial version.

    Use the template algorithm/algorithm_form.html
    """

    model = Algorithm
    fields = ['name','description','topic']
    success_url = reverse_lazy('algorithm:index')

    def form_valid(self, form):
        """Create an initial version for the algorithm.

        This method is called when valid form data has been POSTed.
        """
        
        # Relate current user with the created algorthm
        form.instance.created_by = self.request.user
        self.object = form.save()

        # Creating new algorithm version
        version = Version(
            algorithm=self.object ,
            description='Versión por defecto 1.0',
            number='1.0',
            repository_url='',
            publishing_state=Version.DEVELOPED_STATE
        )
        version.save()
        return redirect(self.get_success_url())
 
    def get_context_data(self, **kwargs):
        """Add or change context initial data."""

        data = super(AlgorithmCreateView, self).get_context_data(**kwargs)
        topics = Topic.objects.filter(enabled=True)
        data['algorithm_form'] = data.get('form')
        data['topics'] = topics

        # Template aditional data
        data['section'] = 'Nuevo'
        data['title'] = 'Nuevo Algoritmo'
        data['button'] = 'Crear Algoritmo'
        return data


class AlgorithmUpdateView(UpdateView):
    """Update an algorithm.

    Use the template algorithm/algorithm_form.html
    """

    model = Algorithm
    fields = ['name','description','topic']
    success_url = reverse_lazy('algorithm:index')


    def get_context_data(self, **kwargs):
        """Add or change context initial data."""

        data = super(AlgorithmUpdateView, self).get_context_data(**kwargs)
        topics = Topic.objects.filter(enabled=True)
        data['algorithm_form'] = data.get('form')
        data['topics'] = topics

        # Template aditional data
        data['section'] = 'Editar'
        data['title'] = 'Editar Algoritmo'
        data['button'] = 'Actualizar Algoritmo'
        return data


class AlgorithmDetailView(DetailView):
    """Display algorithm detail.

    Use the template algorithm/algorithm_detail.html
    """
    model = Algorithm
    context_object_name = 'algorithm'


class VersionCreateView(CreateView):
    """Create a version for a given algorithm.

    Use the template algorithm/version_form.html
    """
    model = Version

    def get_context_data(self, **kwargs):
        """Add or change context initial data."""

        data = super(VersionUpdateView, self).get_context_data(**kwargs)
        data['version_form'] = data.get('form')
        return data


class VersionDetailView(DetailView):
    """Display version detail.

    Use the template algorithm/version_detail.html
    """
    model = Version


class VersionUpdateView(UpdateView):
    """Perform version update.

    Use the template algorithm/version_form.html
    """
    model = Version

    def get_context_data(self, **kwargs):
        """Add or change context initial data."""

        data = super(VersionUpdateView, self).get_context_data(**kwargs)
        data['version_form'] = data.get('form')
        return data

    def get_initial(self):
        """This method must return a dictionary."""

        last_version_pk = self.kwargs.get('pk')
        last_version = get_object_or_404(Version,pk=last_version_pk)
        data = { 'version': last_version }
        return data
