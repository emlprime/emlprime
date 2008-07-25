from django.http import HttpResponseRedirect
from django.core.mail import mail_admins

from emlprime.static.models import Project
from emlprime.static.forms import ProjectForm
from emlprime.common.decorators import ajax_or_http_response

@ajax_or_http_response
def detail(request):
    """ Creates a project using the project form
    """
    template = "work.html"
    if request.method == 'POST':
        values = request.POST.copy()
        form = ProjectForm(values)
        if form.is_valid():
            project=form.save()
#            mail_admins('Project Request Submitted', 'project.name, project.email, project.description', fail_silently=False)
            return HttpResponseRedirect("/work/create/")
        else:
            errors=form.errors
    else:
        form = ProjectForm()
    return locals()

@ajax_or_http_response
def create(request):
    """ Redirects to thank-you page following project object creation
    """
    return HttpResponseRedirect("/work/create/")

@ajax_or_http_response
def confirmation(request):
    """ Confirms the project request
    """
    template = "project_create.html"
    return locals()
