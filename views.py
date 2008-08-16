from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import mail_admins
from django.utils import simplejson
from random import choice

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
            message =  "%s\n%s\n%s" % (project.name, project.email, project.description)
            mail_admins('Project Request Submitted', message, fail_silently=False)
            return HttpResponseRedirect("/work/create/")
        else:
            errors=form.errors
    else:
        form = ProjectForm()
    return locals()

@ajax_or_http_response
def confirmation(request):
    """ Confirms the project request
    """
    template = "project_create.html"
    return locals()

@ajax_or_http_response
def play(request):
    """ Provides a sequence of 50 colors for the game
    """
    template = "play.html"    
    return locals()

def get_answer_key(request):
    # lists the colors available
    colors = ["red", "green", "blue", "yellow"]
    # generates a random sequence of 50 colors
    answer_key = [choice(colors) for i in range(5)]
    json_answer_key = simplejson.dumps(answer_key)
    
    return HttpResponse(json_answer_key, mimetype="application/json")

@ajax_or_http_response
def us(request):
    """ Display info about us
    """
    template = "us.html"
    return locals()

@ajax_or_http_response
def sample_workflow(request):
    """ Display a sample workflow
    """
    template = "sample_workflow.html"
    return locals()
