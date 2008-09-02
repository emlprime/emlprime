from django.forms.models import ModelForm
from django.forms import forms

from emlprime.static.models import Project

class ProjectForm(ModelForm):
    """ Provides the project request form
    """

    class Meta:
        model = Project

    def save(self, commit=True):
        project = super(ProjectForm, self).save()
        return project
