 # -*- coding: utf-8 -*-

from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound
from django.conf import settings
from django.core.files import File
from django.utils.encoding import smart_str
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils import formats
from django.utils import timezone

from storage.forms import StorageUnitForm
from storage.forms import StorageUnitUpdateForm
from storage.models import StorageUnit

import mimetypes
import requests
import os
import re
import json
import dateutil


@method_decorator(
    permission_required(
        'storage.can_list_units',
        raise_exception=True
    ),
    name='dispatch'
)
class IndexView(LoginRequiredMixin,TemplateView):
    """Render the list of storage units."""
    template_name = 'storage/index.html'


class StoragelistJsonView(TemplateView):
    """Return a list of storage units.

    This view consult the REST API.
    """

    # To allow post requests without CSRF token
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(StoragelistJsonView, self).dispatch(*args, **kwargs)

    def get(self,request,*arg,**kwars):
        """Retrieve the list of storage units from the API."""
        url = "{}/api/storage_units/".format(
            settings.DC_API_URL
        )

        storage_units = self._perfom_request(url)
        for storage_dict in storage_units:
            date_str = storage_dict['created_at']
            date = dateutil.parser.parse(date_str)
            date = timezone.localtime(date)
            date = formats.date_format(date,format='DATETIME_FORMAT')
            storage_dict['created_at'] = date

        # In order to allow non-dict objects to be serialized 
        # set the safe parameter to False.
        return JsonResponse(storage_units,safe=False)

    def post(self,request,*arg,**kwars):
        """
        This method is used by /static/js/formBuilder.js (line 193)
        to get the given storage unit data.
        """

        storage_unit_id = request.POST.get('storage_unit_id')
        url = "{}/api/storage_units/{}".format(
            settings.DC_API_URL, storage_unit_id
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


class StorageObtainJsonListView(View):
    """
    Return a list of the storage units as json objects.
    """

    def get(self,request,*args,**kwargs):
        """
        This method is only used by /static/js/formBuilder.js 
        (lines 438 and 600) to get the given storage unit data.
        """

        version_pk = request.GET.get('version_pk',None)
        if version_pk:
            queryset = StorageUnit.objects.filter(versionstorageunit__version__pk=version_pk)
        else:
            queryset = StorageUnit.objects.all()

        data = serializers.serialize("json", queryset)
        return HttpResponse(data, content_type='application/json')     


@method_decorator(
    permission_required(
        'storage.can_create_units',
        raise_exception=True
    ),
    name='dispatch'
)
class StorageCreateView(LoginRequiredMixin,FormView):
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

        # print('STORAGE FILE',type(description_binary_file),description_binary_file)

        # As strings are objects they can be decoded calling the 'decode' method
        # description_file_str = description_binary_file.read().decode()
        # ingest_file_str = ingest_binary_file.read().decode()
        # metadata_generation_script_file_str = metadata_generation_script_binary_file.read().decode()

        files = {
            'description_file':description_binary_file.file,
            'ingest_file': ingest_binary_file.file,
            'metadata_generation_script': metadata_generation_script_binary_file.file
        }

        data = {
            "alias":alias,
            "name": name,
            "description": description,
            "created_by": self.request.user.id
        }

        # data = json.dumps(data)

        url = "{}/api/storage_units/".format(settings.DC_API_URL)

        response = requests.post(url,data=data,files=files)

        if response.status_code != 201:
            err_message = response.json()
            messages.warning(self.request,
                'Ha ocurrido un error con el envío de la información, por favor vuelve a intentarlo.'
            )
            messages.warning(self.request,err_message)
            return redirect('storage:index')

        return super().form_valid(form)


@method_decorator(
    permission_required(
        'storage.can_edit_units',
        raise_exception=True
    ),
    name='dispatch'
)
class StorageUpdateView(LoginRequiredMixin,UpdateView):
    """Update an algorithm.

    Use the template storage/storage_form.html
    """

    model = StorageUnit
    form_class = StorageUnitUpdateForm
    template_name = 'storage/storage_update.html'
    success_url = reverse_lazy('storage:index')


@method_decorator(
    permission_required(
        'storage.can_view_unit_detail',
        raise_exception=True
    ),
    name='dispatch'
)
class StorageDetailView(LoginRequiredMixin,DetailView):
    """Display storage unit detail.

    Use the template storage/storage_detail.html
    """
    model = StorageUnit
    context_object_name = 'storage_unit'
    template_name = 'storage/storage_detail.html'


class DownloadFileView(TemplateView):
    """Donwload dc_storage metadata files."""

    def get(self,request,*args,**kwargs):
        """
        Allow the download of the metadata file of a given storage.
        Example:

            LS8_OLI_LEDAPS/ -> Storage 
                ingest_file.yml
                description_file.yml
                mgen_script.py
        """
        storage_unit_id = kwargs.get('pk')
        file_name = kwargs.get('file_name')

        storage_unit = get_object_or_404(StorageUnit,pk=storage_unit_id)

        file_path = os.path.join(
            settings.DC_STORAGE_PATH,storage_unit.name,file_name
        )

        with open(file_path,'rb') as file:
            mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file,content_type=mimetype)
            response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
            return response

        # if the file could not be opened.
        raise Http404



@method_decorator(
    permission_required(
        'storage.can_view_storage_content',
        raise_exception=True
    ),
    name='dispatch'
)
class StorageViewContentView(LoginRequiredMixin,DetailView):
    """
    Show the storage unit content. The storage 
    unit content is actually given by other view 
    (StorageViewContentJsonView)
    thought javascript in the template.
    """

    model = StorageUnit
    template_name = 'storage/storage_content.html'
    context_object_name = 'storage_unit'


@method_decorator(
    permission_required(
        'storage.can_view_storage_content',
        raise_exception=True
    ),
    name='dispatch'
)
class StorageViewContentJsonView(TemplateView):
    """
    Return the content of a given storage unit as json. 
    The storage unit content is obtained by a call to the 
    Rest Api component.
    """

    def get(self,request,*args,**kwargs):
        """Return the content of a given storage unit as json."""
        
        storage_unit_id = kwargs.get('pk')
        path = request.GET.get('path','/years/')

        try:
            json_response = []
            url = "{}/api/storage_units/{}{}".format(settings.DC_API_URL, storage_unit_id, path)
            if url.endswith("/years/"):
                
                fake_url = "http://www.mocky.io/v2/5838bf6511000096168fd3ca"
                response = requests.get(url)
                entries = response.json()["years"]
                for entry in entries:
                    json_object = {
                        'name': "{}".format(entry),
                        'is_dir': True,
                        'is_file': False,
                    }
                    json_response.append(json_object)
            elif re.search('years/([0-9]*)/$', url):
                
                fake_url = "http://www.mocky.io/v2/5838bf921100009c168fd3cb"
                response = requests.get(url)
                entries = response.json()["coordinates"]
                for entry in entries:
                    json_object = {
                        'name': "{}".format(str(entry["longitude"]) + "_" + str(entry["latitude"])),
                        'is_dir': True,
                        'is_file': False,
                    }
                    json_response.append(json_object)
            else:
                
                fake_url = "http://www.mocky.io/v2/5838bfb51100009d168fd3cc"
                response = requests.get(url)
                entries = response.json()["images"]
                for entry in entries:
                    json_object = {
                        'name': "{}".format(entry),
                        'is_dir': False,
                        'is_file': True,
                    }
                    json_response.append(json_object)
            return JsonResponse(json_response, safe=False)
        except:
            raise
            return HttpResponseBadRequest()


@method_decorator(
    permission_required(
        'storage.can_view_content_detail',
        raise_exception=True
    ),
    name='dispatch'
)
class StorageImageDetailView(LoginRequiredMixin,TemplateView):
    """
    Return the content of a given storage unit as json. 
    The storage unit content is obtained by a call to the 
    Rest Api component.
    """

    def get(self,request,*args,**kwargs):
        """Return the content of a given storage unit as json."""
        
        storage_unit_id = kwargs.get('pk')
        image_name = kwargs.get('name')

        url = "{}/api/storage_units/{}/contents/{}/".format(
            settings.DC_API_URL, storage_unit_id, image_name
        )
        
        response = requests.get(url)
        image_info = response.json()
        year = image_info["year"]
        coordinates = image_info["coordinates"]
        name = image_info["image_name"]
        storage_unit_alias = image_info["storage_unit_alias"]
        image_storage_unit = image_info["storage_unit"]
        thumbnails = image_info["thumbnails"]
        metadata = json.dumps(image_info["metadata"], indent=4, sort_keys=True)
        
        context = {
            'metadata': metadata, 
            'thumbnails': thumbnails, 
            'year': year, 
            'coordinates': coordinates, 
            'name': name,
            'image_storage_unit': image_storage_unit, 
            'storage_unit_alias': storage_unit_alias,
            'image_name': image_name, 
            'storage_unit_id': storage_unit_id
        }

        return render(request, 'storage/image_detail.html', context)


@method_decorator(
    permission_required(
        'storage.can_download_file',
        raise_exception=True
    ),
    name='dispatch'
)
class StorageDownloadImageView(LoginRequiredMixin,TemplateView):
    """Download an image form the given storage unit and image name.

    The image is downloaded from the dc_storage/<product-name>/...image_name
    """

    def get(self,request,*args,**kwargs):
        """
        Allow the downloading of a .nc image of a given product
        form the dc_storage
        """

        storage_unit_id = kwargs.get('pk')
        image_name = kwargs.get('image_name')

        url = "{}/api/storage_units/{}/contents/{}/".format(
            settings.DC_API_URL, storage_unit_id, image_name
        )

        response = requests.get(url)
        image_info = response.json()

        file_path = image_info["image_uri"]
        file_name = file_path.split('/')[-1]

        with open(file_path,'rb') as file:
            mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file,content_type=mimetype)
            response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
            return response

        # if the file could not be opened.
        return HttpResponseNotFound('<h1>El archivo no se ha encontrado en el servidor</h1>')


@method_decorator(
    permission_required(
        'storage.can_download_metadata',
        raise_exception=True
    ),
    name='dispatch'
)
class StorageDownloadImageMetadataJsonView(LoginRequiredMixin,TemplateView):
    """Download an image metadata as json."""

    def get(self,request,*args,**kwargs):
        """
        Return the metadata of a given image contained in a 
        given storage unit as json object.
        """

        storage_unit_id = kwargs.get('pk')
        image_name = kwargs.get('name')

        url = "{}/api/storage_units/{}/contents/{}/".format(
            settings.DC_API_URL, storage_unit_id, image_name
        )
        
        response = requests.get(url)
        image_info = response.json()
        metadata = json.dumps(image_info["metadata"], indent=4, sort_keys=True)
        return HttpResponse(metadata, content_type='application/json')
