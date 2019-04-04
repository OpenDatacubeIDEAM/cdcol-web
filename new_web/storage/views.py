 # -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings

from storage.forms import StorageUnitForm
from storage.models import StorageUnit

from io import StringIO
import requests
import json
import base64


class IndexView(TemplateView):
    """Render the list of storage units."""
    template_name = 'storage/index.html'


class StoragelistJsonView(TemplateView):
    """Return a list of storage units.

    This view consult the REST API.
    """

    def get(self,request,*arg,**kwars):
        """Retrieve the list of storage units from the API."""
        url = "{}/api/storage_units/".format(
            settings.API_URL
        )

        storage_units = self._perfom_request(url)

        # In order to allow non-dict objects to be serialized 
        # set the safe parameter to False.
        return JsonResponse(storage_units,safe=False)

    def post(self,request,*arg,**kwars):
        """This method is not used"""
        storage_unit_id = request.POST.get('storage_unit_id')
        url = "{}/api/storage_units/{}".format(
            settings.API_URL, storage_unit_id
        )

        storage_units = self._perfom_request(url)

        # In order to allow non-dict objects to be serialized 
        # set the safe parameter to False.
        return JsonResponse(storage_units,safe=False)

    def _perfom_request(self,url):
        """Perform the request and check for errors."""

        try:
            response = requests.get(url)
            storage_units = response.json()

            if response.status_code != 200:
                raise Exception()
        except: 
            messages.warning(
                self.request,
                'La API REST esta fallando o esta inactiva.'
            )
            storage_units = []

        return storage_units


class StorageCreateView(FormView):
    """ Create a storage unit for the datacube.
    
    Tell to the REST API to create a storage unit.
    """
    template_name = 'storage/storage_form.html'
    form_class = StorageUnitForm
    success_url = reverse_lazy('storage:index')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        alias = form.cleaned_data['alias']
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']

        # In Python 3 Files are binary files, this files can not be serialized.
        description_binary_file = form.cleaned_data['description_file']
        ingest_binary_file = form.cleaned_data['ingest_file']
        metadata_generation_script_binary_file = form.cleaned_data['metadata_generation_script']

        # As strings are objects they can be decoded calling the 'decode' method
        description_file_str = description_binary_file.read().decode()
        ingest_file_str = ingest_binary_file.read().decode()
        metadata_generation_script_file_str = metadata_generation_script_binary_file.read().decode()

        data = {
            "alias":alias,
            "name": name,
            "description": description,
            "description_file": description_file_str,
            "ingest_file": ingest_file_str,
            "metadata_generation_script": metadata_generation_script_file_str,
            "created_by": self.request.user.id
        }

        header = {'Content-Type': 'application/json'}
        url = "{}/api/storage_units/".format(settings.API_URL)
        response = requests.post(url, data=json.dumps(data), headers=header)

        print('JSON',json.dumps(data))

        if response.status_code != 201:
            err_message = response.json()[0]
            messages.warning(self.request,
                'Ha ocurrido un error con el envío de la información, por favor vuelve a intentarlo.'
            )
            messages.warning(self.request,err_message)
            return redirect('storage:index')

        return super().form_valid(form)


class StorageDetailView(DetailView):
    """Display storage unit detail.

    Use the template storage/storage_detail.html
    """
    model = StorageUnit
    context_object_name = 'storage_unit'
    template_name = 'storage/storage_detail.html'


class DownloadFileView(TemplateView):

    def get(self,request,*args,**kwargs):

        storage_unit_id = kwargs.get('pk')
        file_name = kwargs.get('file_name')

        print('storage_unit',storage_unit_id)
        print('file',file_name)
