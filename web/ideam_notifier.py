# -*- coding: utf-8 -*-
import os
import django
import sys

reload(sys)
sys.setdefaultencoding("utf8")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ideam_cdc.settings")
django.setup()

from execution.models import Execution
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import socket
from django.core.urlresolvers import reverse


def send_mail(execution):
	"""
	Sends notification to the user
	:param execution:
	:return:
	"""
	try:
		execution_link = "http://{}{}".format(socket.gethostbyname(socket.gethostname()),
		                                      reverse('execution:detail', kwargs={'execution_id': execution.id}))
		subject, from_email, to = 'Notificación de Ejecución', settings.DEFAULT_FROM_EMAIL, execution.executed_by.email
		text_content = "Hola {}, \n\n La ejecución #{} que solicitó ha finalizado en estado: {}. \n\n Ingrese al siguiente link para conocer más información: {}".format(
			execution.executed_by.first_name, execution.id, execution.get_state_display(), execution_link)
		html_content = "<h1>Hola {}</h1>" \
		               "<br>" \
		               "<p>La ejecución #{} que solicitó ha finalizado en estado: <strong>{}</strong> <p>" \
		               "<br>" \
		               "Ingrese al siguiente link para conocer más información: <a href='{}'>{}</a></p>".format(
			execution.executed_by.first_name, execution.id, execution.get_state_display(), execution_link, execution_link)
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		print "....Enviando correo de notificación al usuario {}".format(execution.executed_by.email)
		msg.attach_alternative(html_content, "text/html")
		msg.send()
	except Exception, e:
		print "Ha ocurrido un error enviando el correo. {}".format(e)


def send_notifications():
	"""
	Filter all the completed or with an error to notify the user
	:return:
	"""
	print "Revisando ejecuciones pendientes por enviar..."
	executions = Execution.objects.filter(
		Q(email_sent=False) &
		(Q(state=Execution.COMPLETED_STATE) | Q(state=Execution.ERROR_STATE)))
	for execution in executions:
		print "...Analizando ejecución {}".format(execution.id)
		send_mail(execution)
		execution.email_sent = True
		execution.save()
	print "Proceso terminado"


send_notifications()
