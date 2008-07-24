from django.newforms.models import ModelForm
from django.newforms import forms

from emlprime.static.models import Project

class ProjectForm(ModelForm):
    """ Provides the project request form
    """

    class Meta:
        model = Project

    def save(self, commit=True):
        project = super(PromptForm, self).save()
        return project
