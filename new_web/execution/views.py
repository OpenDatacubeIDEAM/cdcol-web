# -*- coding: utf-8 -*-

from django.db.models import Avg,Sum
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse

from rest_framework import viewsets
from execution.serializers import ExecutionSerializer
from execution.forms import VersionSelectionForm
from execution.models import Execution
from execution.models import Review
from algorithm.models import VersionStorageUnit
from algorithm.models import Parameter
from algorithm.models import Algorithm
from algorithm.models import Version
from algorithm.models import Topic
from execution.models import StringType
from execution.models import IntegerType
from execution.models import DoubleType
from execution.models import BooleanType
from execution.models import AreaType
from execution.models import StorageUnitBandType
from execution.models import TimePeriodType
from execution.models import FileType
from execution.models import StorageUnitNoBandType

import os
import zipfile

class ExecutionIndexView(TemplateView):
    """Display a list of the algorithms."""
    template_name = 'execution/index.html'

    def get_context_data(self,**kwargs):
    	"""Add extra content data to the context."""
    	context = super(ExecutionIndexView, self).get_context_data(**kwargs)
    	temporizer = settings.WEB_EXECUTION_TEMPORIZER
    	context['temporizer_value'] = temporizer
    	return context


class ExecutionViewSet(viewsets.ModelViewSet):
    """CRUD over Algoritm model via API calls."""
    queryset = Execution.objects.all()
    serializer_class = ExecutionSerializer

    def get_queryset(self):
        """Filter the queryset depending of the user.
        
        Executions created by the current user will be 
        retrieved, but also the 'state' of the retrieved 
        executions must be Execution.ENQUEUED_STATE.
        """
        current_user = self.request.user
        queryset = super().get_queryset().filter(executed_by=current_user)

        return queryset


class AlgorithmsByTopicListView(ListView):
    """List algorithms by topic to be selected for execution."""
    
    model = Topic
    context_object_name = 'topics'
    template_name = 'execution/algorithms_by_topic_list.html'

    def get_queryset(self,**kwargs):
        """
        Return the topic which have algorithms which has 
        some version in published state.
        """
        queryset = super().get_queryset().filter(
            algorithm__version__publishing_state=Version.PUBLISHED_STATE,
            enabled=True
        )
        return queryset


class ExecutionCreateView(TemplateView):
    """
    An execution is created given an algorithm. 
    The last version of the algorithm is always 
    considered on this view to create an Execution.
    """

    def get(self,request,*args,**kwargs):

        # Getting the version to be executed
        version_pk = kwargs.get('pk')
        version = get_object_or_404(Version, pk=version_pk)

        # Current user
        current_user = request.user

        # User approved credits
        credits_approved = current_user.profile.credits_approved
        # User credits consumed
        credits_consumed = current_user.profile.credits_consumed

        if credits_consumed:
            credits_approved -= credits_consumed

        # Version selection form
        version_selection_form = VersionSelectionForm(
            algorithm=version.algorithm,user=request.user
        )

        storage_units_version = VersionStorageUnit.objects.filter(
            version__algorithm=version.algorithm
        )

        parameters = Parameter.objects.filter(
            version=version, enabled=True
        ).order_by('position')

        reviews = Review.objects.filter(execution__version=version)

        # getting the average rating
        average_rating = Review.objects.filter(
            execution__version=version
        ).aggregate(Avg('rating'))['rating__avg']
        average_rating = round(average_rating if average_rating is not None else 0, 2)

        executions = Execution.objects.filter(version=version)

        topics = Topic.objects.filter(enabled=True)

        executed_params = []

        context = {
            'topics': topics, 
            'algorithm': version.algorithm, 
            'parameters': parameters,
            'version_selection_form': version_selection_form, 
            'version': version,
            'reviews': reviews,
            'average_rating': average_rating, 
            'executions': executions,
            'executed_params': executed_params, 
            'credits_approved': credits_approved,
            # return this parameter as a list is mandatory for
            # /static/js/formBuilder.js works properly
            'storage_units_version':list(storage_units_version)
        }

        return render(request, 'execution/execution_form.html', context)

    def post(self,request,*args,**kwargs):

        # Getting the version to be executed
        version_pk = kwargs.get('pk')
        version = get_object_or_404(Version, pk=version_pk)

        # Current user
        current_user = request.user

        # User approved credits
        credits_approved = current_user.profile.credits_approved
        # User credits consumed
        credits_consumed = current_user.profile.credits_consumed

        if credits_consumed:
            credits_approved -= credits_consumed

        parameters = Parameter.objects.filter(
            version=version, enabled=True
        ).order_by('position')

        textarea_name = request.POST.get('textarea_name', None)
        checkbox_generate_mosaic = request.POST.get('checkbox_generate_mosaic', None)
        if checkbox_generate_mosaic is None :
            checkbox_generate_mosaic = False;
      
        if current_user.has_perm('execution.can_create_new_execution'):
            parameter = parameters.get(parameter_type=Parameter.AREA_TYPE)
            time_parameters = parameters.filter(parameter_type=Parameter.TIME_PERIOD_TYPE)
            if parameter and credits_approved:
                anhos = 1
                if time_parameters:
                    anhos = 0
                    for p in time_parameters:
                        start_date = request.POST.get('start_date_{}'.format(p.id), False)
                        end_date = request.POST.get('end_date_{}'.format(p.id), False)
                        start_date_value = datetime.datetime.strptime(start_date, "%d-%m-%Y")
                        end_date_value = datetime.datetime.strptime(end_date, "%d-%m-%Y")
                        anhos += 1+(end_date_value.year - start_date_value.year)
                else:
                    anhos = 1

                sw_latitude = int(request.POST.get('sw_latitude', False))
                sw_longitude = int(request.POST.get('sw_longitude', False))
                ne_latitude = int(request.POST.get('ne_latitude', False))
                ne_longitude = int(request.POST.get('ne_longitude', False))
                credits_calculated = (ne_latitude-sw_latitude)*(ne_longitude-sw_longitude)*anhos
                if credits_calculated <= credits_approved:
                    new_execution = Execution(
                        version=version,
                        description=textarea_name,
                        state=Execution.ENQUEUED_STATE,
                        executed_by=current_user,
                        generate_mosaic= checkbox_generate_mosaic,
                        credits_consumed=credits_calculated,
                    )
                    new_execution.save()

                    create_execution_parameter_objects(parameters, request, new_execution)

                    # Unzip uploaded parameters
                    execution_directory = os.path.join(settings.MEDIA_ROOT,'input',str(new_execution.id))

                    if os.path.isdir(execution_directory):
                        unzip_every_file_in_directory(execution_directory)

                    # send the execution to the REST service
                    response = send_execution(new_execution)

                    print(response)
                    return HttpResponseRedirect(reverse('execution:detail', kwargs={'execution_id': new_execution.id}))


def create_execution_parameter_objects(parameters, request, execution):
    """
    Creates an execution parameter based on the parameter type
    :param parameters: The parameters of the version
    :param request: The HTTP request object
    :return:
    """
    for parameter in parameters:
        if parameter.parameter_type == "1":
            print("Getting elements for String parameter")
            string_name = "string_input_{}".format(parameter.id)
            string_value = request.POST.get(string_name, False)
            # STRING TYPE
            new_execution_parameter = StringType(
                execution=execution,
                parameter=parameter,
                value=string_value
            )
            new_execution_parameter.save()
        if parameter.parameter_type == "2":
            print("Getting elements for Integer parameter")
            integer_name = "integer_input_{}".format(parameter.id)
            integer_value = request.POST.get(integer_name, False)
            # INTEGER TYPE
            new_execution_parameter = IntegerType(
                execution=execution,
                parameter=parameter,
                value=integer_value
            )
            new_execution_parameter.save()
        if parameter.parameter_type == "3":
            print("Getting elements for Double parameter")
            double_name = "double_input_{}".format(parameter.id)
            double_value = request.POST.get(double_name, False)
            # DOUBLE TYPE
            new_execution_parameter = DoubleType(
                execution=execution,
                parameter=parameter,
                value=double_value
            )
            new_execution_parameter.save()
        if parameter.parameter_type == "4":
            print("Getting elements for BooleanType parameter")
            boolean_name = "boolean_input_{}".format(parameter.id)
            boolean_value = request.POST.get(boolean_name, False)
            # BOOLEAN TYPE
            new_execution_parameter = BooleanType(
                execution=execution,
                parameter=parameter,
                value=boolean_value
            )
            new_execution_parameter.save()
        if parameter.parameter_type == "7":
            print("Getting elements for AreaType parameter")
            sw_latitude = request.POST.get('sw_latitude', False)
            sw_longitude = request.POST.get('sw_longitude', False)
            ne_latitude = request.POST.get('ne_latitude', False)
            ne_longitude = request.POST.get('ne_longitude', False)
            # AREA TYPE
            new_execution_parameter = AreaType(
                execution=execution,
                parameter=parameter,
                latitude_start=sw_latitude,
                latitude_end=ne_latitude,
                longitude_start=sw_longitude,
                longitude_end=ne_longitude
            )
            new_execution_parameter.save()
        if parameter.parameter_type == "8":
            print("Getting elements for StorageUnitType (Bands) parameter")
            select_name = "storage_unit_{}".format(parameter.id)
            bands_name = "bands_{}".format(parameter.id)
            select_value = request.POST.get(select_name, False)
            select_value = StorageUnit.objects.get(pk=select_value)
            bands_selected = request.POST.getlist(bands_name, False)
            bands = ""
            for band in bands_selected:
                bands += band + ","
            bands = bands[:-1]
            # STORAGE UNIT BAND TYPE
            new_execution_parameter = StorageUnitBandType(
                execution=execution,
                parameter=parameter,
                storage_unit_name=select_value.name,
                bands=bands
            )
            new_execution_parameter.save()
        if parameter.parameter_type == "9":
            print("Getting elements for TimePeriod parameter")
            start_date_name = "start_date_{}".format(parameter.id)
            end_date_name = "end_date_{}".format(parameter.id)
            start_date_value = request.POST.get(start_date_name, False)
            end_date_value = request.POST.get(end_date_name, False)
            # parsing dates
            start_date_value = datetime.datetime.strptime(start_date_value, "%d-%m-%Y")
            end_date_value = datetime.datetime.strptime(end_date_value, "%d-%m-%Y")
            # TIME PERIOD TYPE
            new_execution_parameter = TimePeriodType(
                execution=execution,
                parameter=parameter,
                start_date=start_date_value,
                end_date=end_date_value
            )
            new_execution_parameter.save()
        if parameter.parameter_type == "12":
            print("Getting elements for File parameter")
            file_name = "file_input_{}".format(parameter.id)
            file_value = request.FILES.get(file_name, False)
            # FILE TYPE
            new_execution_parameter = FileType(
                execution=execution,
                parameter=parameter,
                file=file_value
            )
            new_execution_parameter.save()
        if parameter.parameter_type == "13":
            print("Getting elements for StorageUnitType (NoBands) parameter")
            select_name = "storage_unit_{}".format(parameter.id)
            select_value = request.POST.get(select_name, False)
            select_value = StorageUnit.objects.get(pk=select_value)
            # STORAGE UNIT NO BAND TYPE
            new_execution_parameter = StorageUnitNoBandType(
                execution=execution,
                parameter=parameter,
                storage_unit_name=select_value.name
            )
            new_execution_parameter.save()


def unzip_every_file_in_directory(execution_directory):
    """ Unzip every .zip under the directory, saves its contents in the same directory the .zip was and then eliminates de .zip file."""
    for root, dirs, files in os.walk(execution_directory):
        for file in files:
            zip_file = "/".join( [ root, file ] )
            if zip_file.endswith('.zip') and root != execution_directory:
                with zipfile.ZipFile(zip_file) as file_to_unzip:
                    file_to_unzip.extractall(root)


def send_execution(execution):
    """
    Create a json request and send it to the REST service
    :param execution: Execution to be send
    :return:
    """
    response = {}
    parameters = ExecutionParameter.objects.filter(execution=execution).order_by('parameter__position')
    # getting all the values
    json_parameters = {}
    for parameter in parameters:
        json_parameters[parameter.parameter.function_name] = parameter.obtain_json_values()
    # building the request
    json_response = {
        'execution_id': execution.id,
        'algorithm_name': "{}".format(slugify(execution.version.algorithm.name)),
        'version_id': "{}".format(execution.version.number),
        'parameters': json_parameters,
        'is_gif': False
    }
    # sending the request
    try:
        header = {'Content-Type': 'application/json'}
        if execution.version.algorithm.id == int(settings.IDEAM_ID_ALGORITHM_FOR_CUSTOM_SERVICE):
            json_response['is_gif'] = True
        url = "{}/api/new_execution/".format(settings.API_URL)
        r = requests.post(url, data=json.dumps(json_response), headers=header)
        if r.status_code == 201:
            response = {'status': 'ok', 'description': 'Se envió la ejecución correctamente.'}
        else:
            response = {'status': 'error', 'description': 'Ocurrió un error al enviar la ejecución',
                        'detalle': "{}, {}".format(r.status_code, r.text)}
    except:
        print('Something went wrong when trying to call the REST service')
    return response


class VersionParametersJson(TemplateView):

    def get(self,request,*args,**kwargs):

        version_id = kwargs.get('pk')
        parameters = Parameter.objects.filter(
            version__id=version_id, enabled=True
        ).order_by('position')

        data = serializers.serialize(
            "json", parameters
        )
        return HttpResponse(data, content_type='application/json')