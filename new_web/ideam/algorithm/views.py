 # -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.files.base import ContentFile
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from rest_framework import viewsets
from algorithm.serializers import AlgorithmSerializer

from algorithm.models import Algorithm
from algorithm.models import Version
from algorithm.models import Parameter
from algorithm.models import VersionStorageUnit
from algorithm.forms import VersionCreateForm
from algorithm.forms import VersionUpdateForm
from algorithm.forms import AlgorithmCreateForm
from algorithm.forms import AlgorithmUpdateForm
from storage.models import StorageUnit

import os
import urllib


class AlgorithmIndexView(TemplateView):
    """Display a list of the algorithms."""
    template_name = 'algorithm/index.html'


class AlgorithmViewSet(viewsets.ModelViewSet):
    """CRUD over Algoritm model via API calls."""
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
    """Create an algorithm and an initial version for the algorithm.

    Use the template algorithm/algorithm_form.html
    """

    model = Algorithm
    form_class = AlgorithmCreateForm
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

        context = super(AlgorithmCreateView, self).get_context_data(**kwargs)
        # Template aditional data
        context['section'] = 'Nuevo'
        context['title'] = 'Nuevo Algoritmo'
        context['button'] = 'Crear Algoritmo'
        return context


class AlgorithmUpdateView(UpdateView):
    """Update an algorithm.

    Use the template algorithm/algorithm_form.html
    """

    model = Algorithm
    form_class = AlgorithmUpdateForm
    success_url = reverse_lazy('algorithm:index')


    def get_context_data(self, **kwargs):
        """Add or change context initial data."""

        context = super(AlgorithmUpdateView, self).get_context_data(**kwargs)
        # Template aditional data
        context['section'] = 'Editar'
        context['title'] = 'Editar Algoritmo'
        context['button'] = 'Actualizar Algoritmo'
        return context

    def get_initial(self):
        """initialize the topic of the algorithm."""
        initial = super(AlgorithmUpdateView, self).get_initial()
        algorithm_obj = self.get_object()
        initial['topic'] = algorithm_obj.topic
        return initial


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
    form_class = VersionCreateForm

    def get_context_data(self, **kwargs):
        """Change form and context initial data."""

        context = super(VersionCreateView, self).get_context_data(**kwargs)
        form = context.get('form')

        algorithm_pk = self.kwargs.get('pk')
        algorithm = get_object_or_404(Algorithm,pk=algorithm_pk)
        minor_version = algorithm.next_minor_version()
        major_version = algorithm.next_major_version()

        form.fields.get('number').choices = [
            (minor_version,'Versión Menor - {}'.format(minor_version)),
            (major_version,'Versión Mayor - {}'.format(major_version))
        ]

        # Template aditional data
        context['section'] = 'Version'
        context['title'] = 'Nueva Version'
        context['button'] = 'Crear Version'

        return context

    def get_initial(self):
        """initialize version algorthm."""
        algorithm_pk = self.kwargs.get('pk')
        algorithm = get_object_or_404(Algorithm,pk=algorithm_pk)
        initial = super(VersionCreateView, self).get_initial()
        initial['algorithm'] = algorithm
        return initial

    def form_valid(self, form):
        """Initialice version status and source_code."""

        # Selecting new version publishing_state.
        form.instance.publishing_state = Version.DEVELOPED_STATE
        self.object = form.save()

        # Download source code from github and save it locally.
        file_name = os.path.basename(self.object.repository_url)
        response = urllib.request.urlopen(self.object.repository_url)
        content = response.read()
        response.close()

        self.object.source_code.save(file_name,ContentFile(content))

        # Relate selecetd storage units with the current version
        selected_storage_units = form.cleaned_data['source_storage_units']
        for storage_unit in selected_storage_units:
            version_storage_unit = VersionStorageUnit(
                version=self.object,
                storage_unit=storage_unit
            )

        messages.info(self.request, 'Nueva versión create con éxito !!.')

        return redirect(self.get_success_url())

    def get_success_url(self):
        """Return a URL to the detail of the algorithm."""
        algorithm_pk = self.kwargs.get('pk')
        return reverse('algorithm:detail',kwargs={'pk':algorithm_pk})


class VersionUpdateView(UpdateView):
    """Perform version update.

    Use the template algorithm/version_form.html
    """
    model = Version
    form_class = VersionUpdateForm

    def get_context_data(self, **kwargs):
        """Add or change context initial data."""

        context = super(VersionUpdateView, self).get_context_data(**kwargs)

        # Template aditional data
        context['section'] = 'Version'
        context['title'] = 'Editar Version'
        context['button'] = 'Actualizar Version'
        return context

    def get_initial(self):
        """initialize version algorthm."""
        initial = super(VersionUpdateView, self).get_initial()
        version_obj = self.get_object()
        initial['algorithm'] = version_obj.algorithm
        initial['number'] = version_obj.number
        return initial

    def get_success_url(self):
        """Return a URL to the detail of the updted version."""
        version_pk = self.kwargs.get('pk')
        return reverse('algorithm:version-detail',kwargs={'pk':version_pk})


class VersionDetailView(DetailView):
    """Display version detail.

    Use the template algorithm/version_detail.html
    """
    model = Version


class VersionPublishView(TemplateView):
    """Change the publishing_state of a version as Version.PUBLISHED_STATE

    Only versions with publishing_state == Version.DEVELOPED_STATE 
    can be published.
    """
    
    def get(self,request,*args,**kwargs):
        version_pk = self.kwargs.get('pk')
        version = get_object_or_404(Version,pk=version_pk)

        if version.publishing_state == Version.DEVELOPED_STATE:
            version.publishing_state = Version.PUBLISHED_STATE
            version.save()
            message = "Versión publicada con éxito."
        else:
            message = (
                "No es posible publicar una version"
                " que no esta en estado 'EN DESARROLLO'."
            )
        
        messages.warning(request, message)

        return redirect('algorithm:version-detail',pk=version_pk)


class VersionDeprecateView(TemplateView):
    """Change the publishing_state of a version as Version.DEPRECATED_STATE

    Only versions with publishing_state == Version.PUBLISHED_STATE 
    can be deprecated.
    """

    def get(self,request,*args,**kwargs):
        version_pk = self.kwargs.get('pk')
        version = get_object_or_404(Version,pk=version_pk)

        if version.publishing_state == Version.PUBLISHED_STATE:
            version.publishing_state = Version.DEPRECATED_STATE
            version.save()
            message = "Versión deprecada con éxito."
        else:
            message = (
                "No es posible deprecar una version"
                " que no esta en estado 'PUBLICADA'."
            )
        
        messages.warning(request, message)

        return redirect('algorithm:version-detail',pk=version_pk)


class ParameterCreateView(CreateView):
    """Create a version for a given algorithm.

    Use the template algorithm/parameter_form.html
    """
    model = Version

    def get_context_data(self, **kwargs):
        """Add or change context initial data."""

        data = super(VersionUpdateView, self).get_context_data(**kwargs)
        data['version_form'] = data.get('form')
        return data