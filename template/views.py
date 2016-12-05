import os
import mimetypes
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from template.models import YamlTemplate
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from template.serializers import YamlSerializer


class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""

	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


def as_json(request):
	queryset = YamlTemplate.objects.all()
	serializer = YamlSerializer(queryset, many=True)
	return JSONResponse(serializer.data)


@login_required(login_url='/accounts/login/')
@permission_required('template.can_list_yaml_templates', raise_exception=True)
def index(request):
	templates = YamlTemplate.objects.all()
	context = {'templates': templates}
	return render(request, 'template/index.html', context)


@permission_required('template.can_download_yaml_template', raise_exception=True)
def download_file(request, template_id):
	"""
	Download a file
	:param request:
	:param full_file_name:
	:return:
	"""
	template = get_object_or_404(YamlTemplate, id=template_id)
	full_file_name = template.file.name
	split_file_name = full_file_name.split('/')
	file_name = split_file_name[len(split_file_name) - 1]
	file_path = "{}/{}".format(settings.MEDIA_ROOT, full_file_name)
	file_wrapper = FileWrapper(file(file_path, 'rb'))
	file_mimetype = mimetypes.guess_type(file_path)
	response = HttpResponse(file_wrapper, content_type=file_mimetype)
	response['X-Sendfile'] = file_path
	response['Content-Length'] = os.stat(file_path).st_size
	response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
	return response
