# -*- coding: utf-8 -*-

from django import forms
from django.db.models import Q
from algorithm.models import Version


class VersionSelectionForm(forms.Form):
    version = forms.ModelChoiceField(queryset=None, widget=forms.Select())

    def __init__(self, *args, **kwargs):
        """
        When the form is instantiated, the user must provide the parameters
        as follows: 

        VersionSelectionForm(algorithm_id=algorithm_id, current_user=current_user)
        
        This allow to obtain the parameters in the contructor.
        """

        self.algorithm = kwargs.pop('algorithm')
        self.user = kwargs.pop('user')
        super(VersionSelectionForm, self).__init__(*args, **kwargs)

        # The choice field will display such versions of a given algorithm
        # that are published or were created by the current user.
        self.fields['version'].queryset = Version.objects.filter(
            Q(algorithm=self.algorithm) &
            (Q(publishing_state=Version.PUBLISHED_STATE) | Q(algorithm__created_by=self.user))
        )
