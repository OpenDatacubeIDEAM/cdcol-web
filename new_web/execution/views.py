# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Avg
from django.utils.text import slugify
from django.contrib import messages

from rest_framework import viewsets
from algorithm.models import VersionStorageUnit
from algorithm.models import Parameter
from algorithm.models import Algorithm
from algorithm.models import Version
from algorithm.models import Topic

from execution.serializers import ExecutionSerializer
from execution.forms import VersionSelectionForm
from execution.forms import ReviewForm
from execution.models import FileConvertionTask
from execution.models import ExecutionParameter
from execution.models import Execution
from execution.models import Review
from execution.models import StringType
from execution.models import IntegerType
from execution.models import DoubleType
from execution.models import BooleanType
from execution.models import AreaType
from execution.models import StorageUnitBandType
from execution.models import TimePeriodType
from execution.models import FileType
from execution.models import StorageUnitNoBandType
from execution.models import Task

from storage.models import StorageUnit

import os
import zipfile
import datetime
import requests
import json
import glob
import subprocess


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
                    messages.info(request,response.get('description'))
                    print(response)
                    return redirect('execution:detail', pk=new_execution.id)

            # This is returned when the Area parameter is not given or
            # the user has consumed all the credits
            messages.warning(request,'El usuario no tiene créditos para llevar a cabo esta ejecución')
            messages.info(request,'O la versión del algoritmo no tiene parametro de tipo AREA')
            return redirect('execution:create', pk=version_pk)

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
            boolean_value = True if isinstance(boolean_value, str) else False
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
        if execution.version.algorithm.id == int(settings.WEB_ALGORITHM_ID_FOR_CUSTOM_SERVICE):
            json_response['is_gif'] = True
        url = "{}/api/new_execution/".format(settings.DC_API_URL)
        r = requests.post(url, data=json.dumps(json_response), headers=header)
        if r.status_code == 201:
            response = {'status': 'ok', 'description': 'Se envió la ejecución correctamente.'}
        else:
            response = {'status': 'error', 'description': 'Ocurrió un error al enviar la ejecución',
                        'detalle': "{}, {}".format(r.status_code, r.text)}
    except:
        print('Something went wrong when trying to call the REST service')
    return response


class ExecutionDetailView(DetailView):

    model = Execution

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        execution_id = self.kwargs.get('pk')
        context = get_detail_context(execution_id)
        return context


def get_detail_context(execution_id):
    execution = get_object_or_404(Execution, id=execution_id)
    executed_params = ExecutionParameter.objects.filter(execution=execution).order_by('parameter__position')
    tasks = Task.objects.filter(execution=execution)
    area_param = ExecutionParameter.objects.get(execution=execution, parameter__parameter_type=Parameter.AREA_TYPE)
    time_period_param = ExecutionParameter.objects.filter(execution=execution, parameter__parameter_type=Parameter.TIME_PERIOD_TYPE).order_by('parameter__position')
    time_period_params_string = ""
    for time_period in time_period_param:
        time_period_params_string+='(u{}u{})'.format(time_period.timeperiodtype.start_date.strftime("%d-%m-%Y"), time_period.timeperiodtype.end_date.strftime("%d-%m-%Y") )
    review = Review.objects.filter(execution=execution).last()
    system_path = "{}/results/{}/".format(settings.WEB_STORAGE_PATH, execution.id)
    files = []
    other_files = []

    try:
        algorithm_name= slugify(execution.version.algorithm.name.lower())
        tiff_message = None
        generating_tiff = '0'
        print(int(area_param.areatype.latitude_start))

        for i in range(int(area_param.areatype.latitude_start), int(area_param.areatype.latitude_end)):

            for j in range(int(area_param.areatype.longitude_start), int(area_param.areatype.longitude_end)):
                file_name= '{}_{}_{}_{}_{}_output.nc'.format(algorithm_name, execution.version.number, i, j, time_period_params_string)
                f = {'file': file_name, 'lat': i, 'long': j, 'task_state': '', 'result_state': os.path.exists(system_path+file_name), 'state': False, 'tiff_file': file_name.replace('.nc', '.tiff')}
                if f['result_state']:
                    f['task_state'] = 'Finalizado'
                elif (os.path.exists(system_path+"{}_{}_no_data.lock".format(i,j)))  or (execution.state == Execution.COMPLETED_STATE and not f['result_state']):
                    f['task_state'] = system_path+file_name
                elif execution.state == Execution.ENQUEUED_STATE:
                    f['task_state'] = 'En espera'
                elif execution.state == Execution.EXECUTING_STATE:
                    f['task_state'] = 'En ejecución'
                elif execution.state == Execution.ERROR_STATE:
                    f['task_state'] = 'Falló'
                elif execution.state == Execution.CANCELED_STATE:
                    f['task_state'] = 'Cancelado'
                else:
                    f['task_state'] = 'Sin información dispónible'
                try:
                    convertion_task = FileConvertionTask.objects.get(execution=execution, filename=f['file'])
                    f['state'] = convertion_task.state
                    if f['state'] == '3':
                        tiff_message='Hubo un error generando el archivo Tiff. Por favor, intente de nuevo'
                    elif f['state'] == True:
                        generating_tiff = '1'
                except FileConvertionTask.DoesNotExist:
                    pass
                except MultipleObjectsReturned:
                    tiff_message = 'Hubo un error generando el archivo Tiff. Por favor, intente de nuevo'
                    FileConvertionTask.objects.filter(execution=execution, filename=f['file']).delete()
                files.append(f)

        if os.path.exists(system_path):
            for f in os.listdir(system_path):
                if ".gif" in f :
                    f = {'file': f, 'state':False}
                    other_files.append(f)
                elif "mosaic" in f and ".nc" in f:
                    f = {'file': f, 'state': False, 'tiff_file':f.replace('.nc', '.tiff')}
                    try:
                        convertion_task = FileConvertionTask.objects.get(execution=execution, filename=f['file'])
                        f['state'] = convertion_task.state
                        if f['state'] == '3':
                            tiff_message = 'Hubo un error generando el archivo Tiff. Por favor, intente de nuevo'
                        elif f['state'] == True:
                            generating_tiff = '1'
                    except ObjectDoesNotExist:
                        pass
                    except MultipleObjectsReturned:
                        tiff_message = 'Hubo un error generando el archivo Tiff. Por favor, intente de nuevo'
                        FileConvertionTask.objects.filter(execution=execution, filename=f['file']).delete()
                    other_files.append(f)


        # for f in os.listdir(system_path):
        #     if ".tiff" not in f:
        #         f = {'file': f, 'lat':0, 'long':0, 'state': False, 'tiff_file': f.replace('.nc', '.tiff')}
        #         try:
        #             convertion_task = FileConvertionTask.objects.get(execution=execution, filename=f['file'])
        #             f['state'] = convertion_task.state
        #         except ObjectDoesNotExist:
        #             pass
        #         except MultipleObjectsReturned:
        #             FileConvertionTask.objects.filter(execution=execution, filename=f['file']).delete()
        #         files.append(f)
    except:
        raise
        pass
    # getting current executions
    current_executions = execution.pending_executions
    # getting temporizer value
    temporizer_value = settings.WEB_EXECUTION_TEMPORIZER
    # getting the delete time
    delete_hours = int(settings.WEB_DAYS_ELAPSED_TO_DELETE_EXECUTION_RESULTS) * 24
    if execution.finished_at:
        delete_time = execution.finished_at + datetime.timedelta(hours=delete_hours)
    else:
        delete_time = None
    context = {'execution': execution, 'executed_params': executed_params, 'review': review, 'files': files, 'other_files': other_files,
               'current_executions': current_executions, 'temporizer_value': temporizer_value, 'delete_time': delete_time,
               'system_path': system_path, 'area_param':area_param, 'time_period_param':time_period_param, 'tiff_message':tiff_message, 'generating_tiff': generating_tiff}
    return context


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


class DeleteResultView(View):

    def get(self,request,*args,**kwargs):

        execution_id = kwargs.get('pk')
        image_name = kwargs.get('image_name')

        if image_name == "all":
            file_path = "{}/results/{}/{}".format(
                settings.WEB_STORAGE_PATH, execution_id, ""
            )
        else:
            splitted_image_name = image_name.split(".")
            splitted_image_name[-1] = "*"
            image_name = ".".join(splitted_image_name)
            file_path = "{}/results/{}/{}".format(
                settings.WEB_STORAGE_PATH, execution_id, image_name
            )
        for file in glob.glob(file_path):
            file = file.replace("(","\(")
            file = file.replace(")","\)")
            subprocess.Popen("rm -rf %s" % file, shell=True)
        while glob.glob(file_path):
                time.sleep(0.5)

        context = get_detail_context(execution_id)
        return redirect(request, 'execution/detail.html', context)


class ExecutionRateView(CreateView):

    model = Review
    form_class = ReviewForm
    template_name = 'execution/execution_rate.html'

    # def get_initial(self):
    #     """initialize the topic of the algorithm."""
    #     initial = super(AlgorithmUpdateView, self).get_initial()
    #     algorithm_obj = self.get_object()
    #     initial['topic'] = algorithm_obj.topic
    #     return initial

    def form_valid(self, form):
        """Create an initial version for the algorithm.

        This method is called when valid form data has been POSTed.
        """
        
        # Relate current user with the created algorthm
        execution_id = self.kwargs.get('pk')
        execution = get_object_or_404(Execution,id=execution_id)

        form.instance.execution = execution
        form.instance.created_by = self.request.user
        self.object = form.save()
        return redirect(self.get_success_url())


class ExecutionCopyView(View):

    def get(self,request,*args,**kwargs):
        pass