# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Avg, Q
from django.utils.encoding import smart_str
from algorithm.models import Topic, Algorithm, VersionStorageUnit
from execution.models import *
from execution.forms import VersionSelectionForm, ReviewForm
from execution.serializers import ExecutionSerializer
from user_profile.models import  *
import datetime
from storage.models import StorageUnit
from rest_framework.renderers import JSONRenderer
from django.conf import settings
import requests
import json
import os , zipfile
import mimetypes
from wsgiref.util import FileWrapper
from slugify import slugify
import subprocess
import glob
import time
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned




class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def as_json(request):
    current_user = request.user
    queryset = Execution.objects.filter(executed_by=current_user)
    serializer = ExecutionSerializer(queryset, many=True)
    for execution in serializer.data:
        execution["can_rate"] = current_user.has_perm('execution.can_rate_execution')
    return JSONResponse(serializer.data)


@login_required(login_url='/accounts/login/')
@permission_required('execution.can_list_executions', raise_exception=True)
def index(request):
    current_user = request.user
    executions = Execution.objects.filter(Q(executed_by=current_user), Q(state=Execution.ENQUEUED_STATE))
    # getting temporizer value
    temporizer_value = settings.IDEAM_TEMPORIZER
    context = {'executions': executions, 'temporizer_value': temporizer_value}
    return render(request, 'execution/index.html', context)


def download(file_path):
    try:
        file_name = file_path.split('/')[-1]
        file_wrapper = FileWrapper(file(file_path, 'rb'))
        file_mimetype = mimetypes.guess_type(file_path)
        response = HttpResponse(file_wrapper, content_type=file_mimetype)
        response['X-Sendfile'] = file_path
        response['Content-Length'] = os.stat(file_path).st_size
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
        return response
    except:
        return HttpResponseNotFound('<h1>El archivo no se ha encontrado en el servidor</h1>')



def download_result(request, execution_id, image_name):
    execution = get_object_or_404(Execution, id=execution_id)
    file_path = "{}/results/{}/{}".format(settings.WEB_STORAGE_PATH, execution.id, image_name)
    return download(file_path)



def download_parameter_file(request, execution_id, parameter_name, file_name):
    execution = get_object_or_404(Execution, id=execution_id)
    file_path = "{}/input/{}/{}/{}".format(settings.MEDIA_ROOT, execution.id, parameter_name, file_name)
    return download(file_path)


def get_detail_context(execution_id):
    execution = get_object_or_404(Execution, id=execution_id)
    executed_params = ExecutionParameter.objects.filter(execution=execution)
    tasks = Task.objects.filter(execution=execution)
    area_param = ExecutionParameter.objects.get(execution=execution, parameter__parameter_type=Parameter.AREA_TYPE)
    time_period_param = ExecutionParameter.objects.get(execution=execution, parameter__parameter_type=Parameter.TIME_PERIOD_TYPE)
    review = Review.objects.filter(execution=execution).last()
    system_path = "{}/results/{}/".format(settings.WEB_STORAGE_PATH, execution.id)
    files = []

    # for task in tasks:
    #     kwargs = json.load(task.parameters)
    #     f = {'file': file_name, 'lat': kwargs['min_lat'], 'long': kwargs['min_long'], 'task_state': task.state,
    #          'result_state': os.path.exists(system_path + file_name), 'state': False,
    #          'tiff_file': file_name.replace('.nc', '.tiff')}

    try:
        algorithm_name= execution.version.algorithm.name.lower().replace(" ", "_")
        tiff_message = None
        generating_tiff = '0'
        for i in range(int(area_param.areatype.latitude_start), int(area_param.areatype.latitude_end)):
            for j in range(int(area_param.areatype.longitude_start), int(area_param.areatype.longitude_end)):
                file_name= '{}_{}_{}_{}_(u{}u{})_output.nc'.format(algorithm_name, execution.version.number, i, j, time_period_param.timeperiodtype.start_date.strftime("%d-%m-%Y"), time_period_param.timeperiodtype.end_date.strftime("%d-%m-%Y"))
                f = {'file': file_name, 'lat': i, 'long': j, 'task_state': '', 'result_state': os.path.exists(system_path+file_name), 'state': False, 'tiff_file': file_name.replace('.nc', '.tiff')}
                if f['result_state']:
                    f['task_state'] = 'Finalizado'
                elif (os.path.exists(system_path+"{}_{}_no_data.lock".format(i,j)))  or (execution.state == Execution.COMPLETED_STATE and not f['result_state']):
                    f['task_state'] = 'Sin datos en el area'
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
                except ObjectDoesNotExist:
                    pass
                except MultipleObjectsReturned:
                    tiff_message = 'Hubo un error generando el archivo Tiff. Por favor, intente de nuevo'
                    FileConvertionTask.objects.filter(execution=execution, filename=f['file']).delete()
                files.append(f)
            other_files = []
            for f in os.listdir(system_path):
                if ".gif" in f :
                    f = {'file': f, 'state':False}
                    other_files.append(f)
                elif "mosaic" in f and ".nc" in f:
                    f = {'file': f, 'state': False}
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
        pass
    # getting current executions
    current_executions = execution.pending_executions
    # getting temporizer value
    temporizer_value = settings.IDEAM_TEMPORIZER
    # getting the delete time
    delete_hours = int(settings.DAYS_ELAPSED_TO_DELETE_EXECUTION_RESULTS) * 24
    if execution.finished_at:
        delete_time = execution.finished_at + datetime.timedelta(hours=delete_hours)
    else:
        delete_time = None
    context = {'execution': execution, 'executed_params': executed_params, 'review': review, 'files': files, 'other_files': other_files,
               'current_executions': current_executions, 'temporizer_value': temporizer_value, 'delete_time': delete_time,
               'system_path': system_path, 'area_param':area_param, 'time_period_param':time_period_param, 'tiff_message':tiff_message, 'generating_tiff': generating_tiff}
    return context


def generate_geotiff(request, execution_id, image_name):
    execution = get_object_or_404(Execution, id=execution_id)
    file_path = "{}/results/{}/{}".format(settings.WEB_STORAGE_PATH, execution.id, image_name)
    # creating the json request
    json_request = {
        'file_path': file_path
    }
    # sending the request
    try:
        response_message = None
        header = {'Content-Type': 'application/json'}
        url = "{}/api/download_geotiff/".format(settings.API_URL)
        # url = "http://www.mocky.io/v2/587e480e100000c114987d96" # 200
        # url = "http://www.mocky.io/v2/587e47b2100000ca14987d95" # 400
        r = requests.post(url, data=json.dumps(json_request), headers=header)
        print r #delete
        json_response = r.json()
        print json_response #delete
        if r.status_code == 200:
            print '200...' # delete
            response_file_path = json_response["file_path"]
            print response_file_path
            if response_file_path:
                file_name = response_file_path.split('/')[-1]
                return download_result(request, execution_id, file_name)
        else:
            print '400...'
            response_message = json_response["message"]
        # setting all the context
        context = get_detail_context(execution_id)
        context['response_message'] = response_message
        return render(request, 'execution/detail.html', context)
    except Exception, e:
        print e
        return HttpResponseNotFound('<h1>Ha ocurrido un error en la conversión</h1>')


@login_required(login_url='/accounts/login/')
@permission_required('execution.can_view_execution_detail', raise_exception=True)
def detail(request, execution_id):
    context = get_detail_context(execution_id)
    return render(request, 'execution/detail.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('execution.can_view_blank_execution', raise_exception=True)
def  new_blank_execution(request):
    topics = Topic.objects.filter(enabled=True)
    context = {'topics': topics}
    return render(request, 'execution/new_blank.html', context)


@login_required(login_url='/accounts/login/')
def obtain_parameters(request, version_id):
    data = serializers.serialize(
        "json", Parameter.objects.filter(version__id=version_id, enabled=True).order_by('position'))
    return HttpResponse(data, content_type='application/json')


def create_execution_parameter_objects(parameters, request, execution, current_version):
    """
    Creates an execution parameter based on the parameter type
    :param parameters: The parameters of the version
    :param request: The HTTP request object
    :return:
    """
    for parameter in parameters:
        if parameter.parameter_type == "1":
            print "Getting elements for String parameter"
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
            print "Getting elements for Integer parameter"
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
            print "Getting elements for Double parameter"
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
            print "Getting elements for BooleanType parameter"
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
            print "Getting elements for AreaType parameter"
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
            print "Getting elements for StorageUnitType (Bands) parameter"
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
            print "Getting elements for TimePeriod parameter"
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
            print "Getting elements for File parameter"
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
            print "Getting elements for StorageUnitType (NoBands) parameter"
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


def send_execution(execution):
    """
    Create a json request and send it to the REST service
    :param execution: Execution to be send
    :return:
    """
    response = {}
    parameters = ExecutionParameter.objects.filter(execution=execution)
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
        print 'Something went wrong when trying to call the REST service'
    return response

def unzip_every_file_in_directory(execution_directory):
    """ Unzip every .zip under the directory, saves its contents in the same directory the .zip was and then eliminates de .zip file."""
    for root, dirs, files in os.walk(execution_directory):
        for file in files:
            zip_file = "/".join( [ root, file ] )
            if zip_file.endswith('.zip') and root != execution_directory:
                with zipfile.ZipFile(zip_file) as file_to_unzip:
                    file_to_unzip.extractall(root)


@login_required(login_url='/accounts/login/')
@permission_required(('execution.can_create_new_execution', 'execution.can_view_new_execution'), raise_exception=True)
def new_execution(request, algorithm_id, version_id, copy_execution_id = 0):
    executed_params = []
    user_profile = []
    if copy_execution_id:
        print copy_execution_id
        executed_params = map(lambda param: param.obtain_json_values(),get_detail_context(copy_execution_id)['executed_params'])
        executed_params = json.dumps(executed_params)
        print executed_params
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user)
    algorithm = get_object_or_404(Algorithm, id=algorithm_id)
    current_version = None
    if version_id:
        current_version = get_object_or_404(Version, id=version_id)
    parameters = Parameter.objects.filter(version=current_version, enabled=True).order_by('position')
    allowed_storage_units = VersionStorageUnit.objects.filter(version=current_version)
    reviews = Review.objects.filter(version=current_version)
    # getting the average rating
    average_rating = Review.objects.filter(version=current_version).aggregate(Avg('rating'))['rating__avg']
    average_rating = round(average_rating if average_rating is not None else 0, 2)
    executions = Execution.objects.filter(version=current_version)
    topics = Topic.objects.filter(enabled=True)
    if request.method == 'POST':
        version_selection_form = VersionSelectionForm(algorithm_id=algorithm_id, current_user=current_user)
        textarea_name = request.POST.get('textarea_name', None)
        checkbox_generate_mosaic = request.POST.get('checkbox_generate_mosaic', None)
        if checkbox_generate_mosaic is None :
            checkbox_generate_mosaic = False;
       # started_at = datetime.datetime.now()

        if current_user.has_perm('execution.can_create_new_execution'):
            parameter = parameters.get(parameter_type=Parameter.AREA_TYPE)

            if parameter and user_profile:

                sw_latitude = request.POST.get('sw_latitude', False)
                sw_longitude = request.POST.get('sw_longitude', False)
                ne_latitude = request.POST.get('ne_latitude', False)
                ne_longitude = request.POST.get('ne_longitude', False)
                credits_calculated = (ne_latitude-sw_latitude)*(ne_longitude-sw_longitude)
                if credits_calculated <= user_profile.credits_approved:
                    new_execution = Execution(
                        version=current_version,
                        description=textarea_name,
                        state=Execution.ENQUEUED_STATE,
                        executed_by=current_user,
                        generate_mosaic= checkbox_generate_mosaic,
                        credits_consumed=credits_calculated,
                    )
                    new_execution.save()

                    create_execution_parameter_objects(parameters, request, new_execution, current_version)

                    # Unzip uploaded parameters
                    execution_directory = "/".join( [ settings.MEDIA_ROOT, 'input', str(new_execution.id) ] )
                    if os.path.isdir(execution_directory):
                        unzip_every_file_in_directory(execution_directory)

                    # send the execution to the REST service
                    response = send_execution(new_execution)

                    print response
                    return HttpResponseRedirect(reverse('execution:detail', kwargs={'execution_id': new_execution.id}))
                else:
                    version_selection_form.add_error(None, "Esta ejecución requiere "+credits_calculated+" créditos y sólo tiene "+user_profile.credits_approved+" créditos disponibles. Disminuya el área o espere a que sus demás ejecuciones finalicen.")
    version_selection_form = VersionSelectionForm(algorithm_id=algorithm_id, current_user=current_user)
    context = {'topics': topics, 'algorithm': algorithm, 'parameters': parameters,
               'version_selection_form': version_selection_form, 'version': current_version,
               'reviews': reviews, 'average_rating': average_rating, 'executions': executions,
               'executed_params': executed_params, 'user_profile': user_profile}
    return render(request, 'execution/new.html', context)


@login_required(login_url='/accounts/login/')
@permission_required('execution.can_rate_execution', raise_exception=True)
def rate_execution(request, execution_id):
    current_user = request.user
    execution = get_object_or_404(Execution, id=execution_id)
    if request.method == 'POST':
        # getting the form
        review_form = ReviewForm(request.POST)
        # checking if the form is valid
        if review_form.is_valid():
            # checking if the execution is able to be rated
            ratings = Review.objects.filter(execution=execution, reviewed_by=current_user)
            if ratings.count() == 0:
                if execution.state == Execution.COMPLETED_STATE or execution.state == Execution.ERROR_STATE:
                    rating = review_form.cleaned_data['rating']
                    comments = review_form.cleaned_data['comments']
                    version = execution.version
                    algorithm = version.algorithm

                    # creating the review
                    new_review = Review(
                        algorithm=algorithm,
                        version=version,
                        execution=execution,
                        rating=rating,
                        comments=comments,
                        reviewed_by=current_user
                    )
                    new_review.save()
                    return HttpResponseRedirect(reverse('execution:index'))
                else:
                    review_form.add_error(None, "No es posible calificar esta ejecución, la ejecución debe haber terminado.")
            else:
                review_form.add_error(None, "No es posible calificar esta ejecución, usted ya ha realizado una calificación a esta.")
        else:
            review_form.add_error(None, "Favor completar todos los campos marcados.")
    else:
        review_form = ReviewForm()
    context = {'review_form': review_form, 'execution': execution}
    return render(request, 'execution/rate.html', context)


@login_required(login_url='/accounts/login/')
def delete_result(request, execution_id, image_name):
        if image_name == "all":
                file_path = "{}/results/{}/{}".format(settings.WEB_STORAGE_PATH, execution_id, "")
        else:
                splitted_image_name = image_name.split(".")
                splitted_image_name[-1] = "*"
                image_name = ".".join(splitted_image_name)
                file_path = "{}/results/{}/{}".format(settings.WEB_STORAGE_PATH, execution_id, image_name)
        for file in glob.glob(file_path):
                file = file.replace("(","\(")
                file = file.replace(")","\)")
                subprocess.Popen("rm -rf %s" % file, shell=True)
        while glob.glob(file_path):
                time.sleep(0.5)
        context = get_detail_context(execution_id)
        return render(request, 'execution/detail.html', context)

def generate_geotiff_task(request, execution_id, image_name):
    execution = get_object_or_404(Execution, id = execution_id)
    new_file_convertion = FileConvertionTask(
        execution = execution,
        filename = image_name,
        state = FileConvertionTask.SCHEDULED_STATE
    )
    new_file_convertion.save()
    return HttpResponseRedirect(reverse('execution:detail', kwargs={'execution_id': execution_id}))

@login_required(login_url='/accounts/login/')
def cancel_execution(request, execution_id):

    Execution.objects.filter(id=execution_id).update(state='5', finished_at=datetime.datetime.now())
    tasks= Task.objects.filter(execution_id=execution_id)
    tasks.update(state='6', state_updated_at=datetime.datetime.now(), end_date=datetime.datetime.now())
    json_request = {
        'execution_id': execution_id
    }
    print 'Este es el id de ejecución {}'.format(execution_id)
    try:
        for t in tasks:
            header = {'Content-Type': 'application/json'}
            url = "{}/api/task/revoke/{}?terminate=true".format("http://34.235.222.79:8082",t.uuid)
            r = requests.post(url, None, headers=header)
            if r.status_code == 200:
                response = {'status': 'ok', 'description': 'Se canceló la ejecución'}
            else:
                response = {'status': 'error', 'description': 'Ocurrió un error al cancelar la ejecución', 'detalle': "{}, {}".format(r.status_code, r.text)}
        # header = {'Content-Type': 'application/json'}
        # url = "{}/api/cancel_execution/".format(settings.API_URL)
        # r = requests.post(url, data=json.dumps(json_request), headers=header)
        # if r.status_code == 200:
        #     response = {'status': 'ok', 'description': 'Se canceló la ejecución'}
        # else:
        #     response = {'status': 'error', 'description': 'Ocurrió un error al cancelar la ejecución',
        #                 'detalle': "{}, {}".format(r.status_code, r.text)}
    except:
        print 'Something went wrong when trying to call the REST service'

    context = get_detail_context(execution_id)
    return render(request, 'execution/detail.html', context)