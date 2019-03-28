 # -*- coding: utf-8 -*-

from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404

from execution.models import Execution
from algorithm.models import Version 


class ExecutionCreateView(CreateView):
    model = Execution

    def get_initial(self):
        """This method must return a dictionary."""

        last_version_pk = self.kwargs.get('pk')
        last_version = get_object_or_404(Version,pk=last_version_pk)
        data = { 'version': last_version }
        return data

