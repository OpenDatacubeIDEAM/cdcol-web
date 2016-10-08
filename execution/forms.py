from django import forms
from algorithm.models import Version


class VersionSelectionForm(forms.Form):
	version = forms.ModelChoiceField(queryset=None, widget=forms.Select(
		attrs={'onChange': "window.location = 'version/' + this.options[this.selectedIndex].value;"}))

	def __init__(self, *args, **kwargs):
		self.algorithm_id = kwargs.pop('algorithm_id')
		super(VersionSelectionForm, self).__init__(*args, **kwargs)
		self.fields['version'].queryset = Version.objects.filter(algorithm__id=self.algorithm_id)
