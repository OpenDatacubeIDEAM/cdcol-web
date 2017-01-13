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


def send_mail(execution):
	"""
	Sends notification to the user
	:param execution:
	:return:
	"""
	try:
		subject, from_email, to = 'Notificación de Ejecución', settings.DEFAULT_FROM_EMAIL, execution.executed_by.email
		text_content = "La ejecución #{} que solicitó ha finalizado en estado: {}".format(execution.id, execution.get_state_display())
		html_content = "<p>La ejecución #{} que solicitó ha finalizado en estado: <strong>{}</strong>".format(execution.id, execution.get_state_display())
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		print "....Enviando correo de notificación al usuario {}".format(execution.executed_by.email)
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
