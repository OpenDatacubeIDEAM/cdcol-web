 # -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.files.base import ContentFile
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormView
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

import django_filters.rest_framework

from rest_framework import viewsets
from algorithm.serializers import AlgorithmSerializer
from algorithm.serializers import VersionSerializer

from algorithm.models import Algorithm
from algorithm.models import Version
from algorithm.models import Parameter
from algorithm.models import VersionStorageUnit
from algorithm.forms import VersionCreateForm
from algorithm.forms import VersionUpdateForm
from algorithm.forms import AlgorithmCreateForm
from algorithm.forms import AlgorithmUpdateForm
from algorithm.forms import VersionPublishForm
from algorithm.forms import ParameterForm
from storage.models import StorageUnit

import os
import urllib
import requests


@method_decorator(
    permission_required('algorithm.can_list_algorithms',raise_exception=True),
    name='dispatch'
)
class AlgorithmIndexView(LoginRequiredMixin,TemplateView):
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


class VersionViewSet(viewsets.ModelViewSet):
    """CRUD over Version model via API calls."""
    queryset = Version.objects.filter(publishing_state__in=['4','5'])
    serializer_class = VersionSerializer


@method_decorator(
    permission_required('algorithm.can_create_algorithm',raise_exception=True),
    name='dispatch'
)
class AlgorithmCreateView(LoginRequiredMixin,CreateView):
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
            algorithm=self.object,
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


@method_decorator(
    permission_required('algorithm.can_edit_algorithm',raise_exception=True)
    ,name='dispatch'
)
class AlgorithmUpdateView(LoginRequiredMixin,UpdateView):
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
        # initial['topic'] = algorithm_obj.topic
        return initial


@method_decorator(
    permission_required('algorithm.can_view_algorithm_detail',raise_exception=True),
    name='dispatch'
)
class AlgorithmDetailView(LoginRequiredMixin,DetailView):
    """Display algorithm detail.

    Use the template algorithm/algorithm_detail.html
    """

    model = Algorithm
    context_object_name = 'algorithm'


@method_decorator(
    permission_required('algorithm.can_create_new_version',raise_exception=True),
    name='dispatch'
)
class VersionCreateView(LoginRequiredMixin,CreateView):
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
        initial['algorithm'] = algorithm.pk
        initial['show_algorthm_name'] = algorithm.name
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

        # Note this doesn’t delete the related objects – it just disassociates them.
        self.object.source_storage_units.clear()
        # Before disassociation, objects can be deleted
        for storage_unit in self.object.source_storage_units.all():
            storage_unit.delete()

        # Relate selecetd storage units with the current version
        selected_storage_units = form.cleaned_data['source_storage_units']
        for storage_unit in selected_storage_units:
            # if not VersionStorageUnit.objects.filter(storage_unit=storage_unit,version=self.object).exists():
            VersionStorageUnit.objects.get_or_create(
                version=self.object,
                storage_unit=storage_unit
            )
            
        messages.info(self.request, 'Nueva versión creada con éxito !!.')

        return redirect(self.get_success_url())

    def get_success_url(self):
        """Return a URL to the detail of the algorithm."""
        algorithm_pk = self.kwargs.get('pk')
        return reverse('algorithm:detail',kwargs={'pk':algorithm_pk})


@method_decorator(
    permission_required('algorithm.can_edit_version',raise_exception=True),
    name='dispatch'
)
class VersionUpdateView(LoginRequiredMixin,UpdateView):
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
        initial['show_algorthm_name'] = version_obj.algorithm.name
        initial['algorithm'] = version_obj.algorithm.pk
        initial['number'] = version_obj.number
        initial['source_storage_units'] = version_obj.source_storage_units.all()
        return initial

    def form_valid(self, form):
        """Initialice version status and source_code."""

        self.object = form.save()

        # Download source code from github and save it locally.
        file_name = os.path.basename(self.object.repository_url)
        response = urllib.request.urlopen(self.object.repository_url)
        content = response.read()
        response.close()

        self.object.source_code.save(file_name,ContentFile(content))

        # Note this doesn’t delete the related objects – it just disassociates them.
        self.object.source_storage_units.clear()
        # Before disassociation, objects can be deleted
        for storage_unit in self.object.source_storage_units.all():
            storage_unit.delete()

        # Relate selecetd storage units with the current version
        selected_storage_units = form.cleaned_data['source_storage_units']
        for storage_unit in selected_storage_units:
            # if not VersionStorageUnit.objects.filter(storage_unit=storage_unit,version=self.object).exists():
            VersionStorageUnit.objects.get_or_create(
                version=self.object,
                storage_unit=storage_unit
            )

        messages.info(self.request, 'Versión actualizada con éxito !!.')

        return redirect(self.get_success_url())

    def get_success_url(self):
        """Return a URL to the detail of the updted version."""
        version_pk = self.kwargs.get('pk')
        return reverse('algorithm:version-detail',kwargs={'pk':version_pk})


@method_decorator(
    permission_required('algorithm.can_view_version_detail',raise_exception=True),
    name='dispatch'
)
class VersionDetailView(LoginRequiredMixin,DetailView):
    """Display version detail.

    Use the template algorithm/version_detail.html
    """
    model = Version


@method_decorator(
    permission_required('algorithm.can_publish_version',raise_exception=True),
    name='dispatch'
)
class VersionPublishView(LoginRequiredMixin,FormView):
    """Change the publishing_state of a version as Version.PUBLISHED_STATE

    Only versions with publishing_state == Version.DEVELOPED_STATE 
    can be published.
    """

    template_name = 'algorithm/algorithm_publish_form.html'
    form_class = VersionPublishForm
    success_url = reverse_lazy('storage:index')


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        version_pk = self.kwargs.get('pk')
        version = get_object_or_404(Version,pk=version_pk)

        template_zip = form.cleaned_data['template']
        algorithms_zip = form.cleaned_data['algorithms']
 
        files = {
            'template_file': template_zip.file,
            'algorithms_zip_file': algorithms_zip.file,
        }

        data = {
            'version_id': version_pk
        }

        url = "{}/api/algorithms/publish/".format(settings.DC_API_URL)

        response = requests.post(url,data=data,files=files)

        if response.status_code != 200:
            err_message = response.json()
            messages.error(self.request,err_message)
            return redirect('algorithm:version-publish',pk=version_pk)

        if version.publishing_state == Version.REVIEW:
            version.publishing_state = Version.PUBLISHED_STATE
            version.save()
            
            message = "Versión publicada con éxito."
            messages.info(self.request, message)

            # send email
            subject = 'Versión Publicada'

            from_email = settings.DEFAULT_FROM_EMAIL
            to_email =  [version.algorithm.created_by.email]

            context = {
                'version':version
            }

            message = render_to_string(
                template_name='algorithm/email/algorithm_published.html',
                context=context,
                request=self.request
            )

            send_mail(subject,message,from_email,to_email,fail_silently=False)

        else:
            message = (
                "No es posible publicar una version "
                "que no esta en estado 'EN REVISION'."
            )
        
            messages.warning(self.request, message)

        return redirect('algorithm:version-detail',pk=version_pk)


@method_decorator(
    permission_required('algorithm.can_unpublish_version',raise_exception=True),
    name='dispatch'
)
class VersionUnPublishView(LoginRequiredMixin,TemplateView):
    """Change the publishing_state of a version as Version.PUBLISHED_STATE

    Only versions with publishing_state == Version.PUBLISHED_STATE,
    and number of Executions == 0 can be unpublished.
    """
    
    def get(self,request,*args,**kwargs):
        version_pk = self.kwargs.get('pk')
        version = get_object_or_404(Version,pk=version_pk)

        # If the algorithm is public
        condition_1 = version.publishing_state == Version.PUBLISHED_STATE
        # and it does not have executions
        condition_2 = version.execution_set.all().count() == 0

        if condition_1 and condition_2:
            version.publishing_state = Version.DEVELOPED_STATE
            version.save()
            message = "Versión ha cambiado a estado 'EN DESARROLLO'."
            messages.info(request, message)
        else:
            message = (
                "No es posible cambiar el estado de la version "
                "puede que tenga ejecuciones o no sea publica aún."
            )
        
            messages.warning(request, message)

        return redirect('algorithm:version-detail',pk=version_pk)


@method_decorator(
    permission_required('algorithm.can_deprecate_version',raise_exception=True),
    name='dispatch'
)
class VersionDeprecateView(LoginRequiredMixin,TemplateView):
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
            messages.info(request, message)
        else:
            message = (
                "No es posible deprecar una version"
                " que no esta en estado 'PUBLICADA'."
            )
        
            messages.warning(request, message)

        return redirect('algorithm:version-detail',pk=version_pk)


# class VersionDeleteView(LoginRequiredMixin,DeleteView):
#     model = Version
#     # success_message = "Versión eliminada con éxito."

#     def get_success_url(self):
#         """
#         Return a URL to the detail of the algorithm which 
#         version was deleted.
#         """
#         algorithm_pk = self.kwargs.get('apk')
#         return reverse('algorithm:detail',kwargs={'pk':algorithm_pk})


@method_decorator(
    permission_required('algorithm.can_delete_version',raise_exception=True),
    name='dispatch'
)
class VersionDeleteView(LoginRequiredMixin,DeleteView):
    """Delete a given version of an algorithm."""
    
    model = Version
    success_message = "Versión eliminada con éxito."

    def get_success_url(self):
        """
        Return a URL to the detail of the algorithm which 
        version was deleted.
        """
        algorithm_pk = self.kwargs.get('apk')
        return reverse('algorithm:detail',kwargs={'pk':algorithm_pk})


@method_decorator(
    permission_required('algorithm.can_send_version_to_review',raise_exception=True),
    name='dispatch'
)
class VersionReviewPendingView(LoginRequiredMixin,TemplateView):
    """Change the publishing_state of a version as Version.REVIEW_PENDING."""
    
    def get(self,request,*args,**kwargs):
        version_pk = self.kwargs.get('pk')
        version = version = get_object_or_404(Version,pk=version_pk)
        version.publishing_state = Version.REVIEW_PENDING
        version.save()

        # send email
        subject = 'Versión Pendiente por Revisión'

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email =  [version.algorithm.created_by.email]

        context = {
            'version':version
        }

        message = render_to_string(
            template_name='algorithm/email/algorithm_review_send.html',
            context=context,
            request=request
        )

        send_mail(subject,message,from_email,to_email,fail_silently=False)

        messages.info(
            request, 
            'La versión del algoritmo esta pendiente por Revisión.'
        )

        return redirect('algorithm:version-detail', pk=version_pk)


@method_decorator(
    permission_required('algorithm.can_start_version_review',raise_exception=True),
    name='dispatch'
)
class VersionReviewStartView(LoginRequiredMixin,TemplateView):
    """Change the publishing_state of a version as Version.REVIEW.

    And send an email to the user to indicate his/her version
    is being reviewed.
    """

    def get(self,request,*args,**kwargs):
        version_pk = self.kwargs.get('pk')
        version = get_object_or_404(Version, pk=version_pk)
        version.publishing_state = Version.REVIEW
        version.save()

        # send email
        subject = 'Versión en Revisión'

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email =  [version.algorithm.created_by.email]

        context = {
            'version':version
        }

        message = render_to_string(
            template_name='algorithm/email/algorithm_review_start.html',
            context=context,
            request=request
        )

        send_mail(subject,message,from_email,to_email,fail_silently=False)

        messages.info(
            request, 
            'Se ha iniciado la revisión de la Version.'
        )

        return redirect('algorithm:version-detail',pk=version_pk)


@method_decorator(
    permission_required('algorithm.can_list_versions',raise_exception=True),
    name='dispatch'
)
class VersionReviewListView(LoginRequiredMixin,TemplateView):
    """Display the list of versions with publishing_state == Version.REVIEW_PENDING"""
    template_name = 'algorithm/version_review_list.html'


@method_decorator(
    permission_required('algorithm.can_create_parameter',raise_exception=True),
    name='dispatch'
)
class ParameterCreateView(LoginRequiredMixin,CreateView):
    """Create a parameter for a given version.

    Use the template algorithm/parameter_form.html
    """
    model = Parameter
    form_class = ParameterForm

    def get_initial(self):
        """initialize version algorthm."""
        initial = super(ParameterCreateView, self).get_initial()
        version_pk = self.kwargs.get('pk')
        version_obj = get_object_or_404(Version,pk=version_pk)
        
        initial['show_algorthm_name'] = version_obj.algorithm.name
        initial['show_version_number'] = version_obj.number

        initial['algorithm'] = version_obj.algorithm.pk
        initial['version'] = version_obj.pk
        return initial

    def get_context_data(self, **kwargs):
        """Add or change context initial data."""

        context = super(ParameterCreateView, self).get_context_data(**kwargs)

        # Template aditional data
        context['section'] = 'Nuevo Parámetro'
        context['title'] = 'Nuevo Parámetro'
        context['button'] = 'Crear Parámetro'
        return context

    def get_success_url(self):
        """
        Return a URL to the detail of the algorithm version.
        """
        version_pk = self.kwargs.get('pk')
        return reverse('algorithm:version-detail',kwargs={'pk':version_pk})


@method_decorator(
    permission_required('algorithm.can_edit_parameter',raise_exception=True),
    name='dispatch'
)
class ParameterUpdateView(LoginRequiredMixin,UpdateView):
    """Update a parameter for a given version.

    Use the template algorithm/parameter_form.html
    """
    model = Parameter
    form_class = ParameterForm

    def get_initial(self):
        """initialize version algorthm."""
        initial = super(ParameterUpdateView, self).get_initial()
        parameter_pk = self.kwargs.get('pk')
        parameter_obj = get_object_or_404(Parameter,pk=parameter_pk)

        initial['show_algorthm_name'] = parameter_obj.version.algorithm.name
        initial['show_version_number'] = parameter_obj.version.number
        
        initial['algorithm'] = parameter_obj.version.algorithm
        initial['version'] = parameter_obj.version
        return initial

    def get_context_data(self, **kwargs):
        """Add or change context initial data."""

        context = super(ParameterUpdateView, self).get_context_data(**kwargs)

        # Template aditional data
        context['section'] = 'Editar Parámetro'
        context['title'] = 'Editar Parámetro'
        context['button'] = 'Actualizar Parámetro'
        return context

    def get_success_url(self):
        """
        Return a URL to the detail of the algorithm version.
        """
        parameter_pk = self.kwargs.get('pk')
        return reverse('algorithm:parameter-detail',kwargs={'pk':parameter_pk})


@method_decorator(
    permission_required('algorithm.can_view_parameter_detail',raise_exception=True),
    name='dispatch'
)
class ParameterDetailView(LoginRequiredMixin,DetailView):
    """Display parameter detail.

    Use the template algorithm/parameter_detail.html
    """
    model = Parameter
    context_object_name = 'parameter'