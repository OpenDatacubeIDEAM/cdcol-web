 # -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings

from storage.forms import StorageUnitForm

import requests


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
        finally:
            storage_units = []

        return storage_units


class StorageCreateView(FormView):
    template_name = 'storage/storage_form.html'
    form_class = StorageUnitForm
    success_url = reverse_lazy('storage:index')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        alias = form.cleaned_data['alias']
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        description_file = request.FILES['description_file']
        ingest_file = request.FILES['ingest_file']
        metadata_generation_script_file = request.FILES['metadata_generation_script']

        print('ingest_file',ingest_file.read())
        print('metadata_generation_script_file',metadata_generation_script_file.read())

        # data = {
        #     "alias":alias,
        #     "name": name,
        #     "description": description,
        #     "description_file": encoded_description,
        #     "ingest_file": encoded_ingest,
        #     "metadata_generation_script": encoded_metadata_script,
        #     "created_by": current_user.id
        # }
        # header = {'Content-Type': 'application/json'}
        # url = "{}/api/storage_units/".format(settings.API_URL)
        # r = requests.post(url, data=json.dumps(data), headers=header)
        # if r.status_code == 201:
        #     return HttpResponseRedirect(reverse('storage:index'))
        # else:
        #     print r.status_code, r.text
        #     form.add_error(None, "Ha ocurrido un error con el envío de la información, por favor vuelve a intentarlo.")

        return super().form_valid(form)