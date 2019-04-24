# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError

from allauth.account.adapter import DefaultAccountAdapter
import re


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
