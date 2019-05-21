# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError

from allauth.account.adapter import DefaultAccountAdapter

import re
import os

class MyAccountAdapter(DefaultAccountAdapter):

    def clean_password(self, password, user=None):
        """Validates a password 

        This function is called when the user reset its password.
        """
        if re.match(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[\S]{8,}$', password):
            return password
        
        message = (
            "La contraseña debe tener mínimo 8 caracteres," 
            " contener minúsculas y mayúsculas."
        )
        raise ValidationError(message)

    def send_mail(self, template_prefix, email, context):
        """
        Change active_url when verification email is sended to the 
        user.
        """
        if hasattr(settings,'WEB_VERIFICATION_EMAIL_URL_PRIFIX'):
            host_port = settings.WEB_VERIFICATION_EMAIL_URL_PRIFIX
            if host_port:
                url = host_port + 'verify-email/' + context['key']
                context['activate_url'] = url

        msg = self.render_mail(template_prefix, email, context)
        msg.send()