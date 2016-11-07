import os
import mimetypes
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from template.models import YamlTemplate
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from django.conf import settings


@login_required(login_url='/accounts/login/')
def index(request):
	templates = YamlTemplate.objects.all()
	context = {'templates': templates}
	return render(request, 'template/index.html', context)


def download_file(request, full_file_name):
	"""
	Download a file
	:param request:
	:param full_file_name:
	:return:
	"""
	split_file_name = full_file_name.split('/')
	file_name = split_file_name[len(split_file_name)-1]
	file_path = "{}/{}".format(settings.MEDIA_ROOT, full_file_name)
	file_wrapper = FileWrapper(file(file_path, 'rb'))
	file_mimetype = mimetypes.guess_type(file_path)
	response = HttpResponse(file_wrapper, content_type=file_mimetype)
	response['X-Sendfile'] = file_path
	response['Content-Length'] = os.stat(file_path).st_size
	response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
	return response