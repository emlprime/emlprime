from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import mail_admins
from django.utils import simplejson
from django.core.paginator import Paginator
from random import choice

from emlprime.static.models import Project, Comic, Portfolio
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
            # try to send mail. If it fails print out an error
            try:
                mail_admins('Project Request Submitted', message, fail_silently=False)
            except:
                print "Error: could not send mail to admins"
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
def game(request):
    """ Provides a sequence of 50 colors for the game
    """
    template = "game.html"    
    return locals()

def get_answer_key(request):
    # lists the colors available
    colors = ["red", "green", "blue", "yellow"]
    # generates a random sequence of 50 colors
    answer_key = [choice(colors) for i in range(50)]
    json_answer_key = simplejson.dumps(answer_key)
    
    return HttpResponse(json_answer_key, mimetype="application/json")

@ajax_or_http_response
def us(request):
    """ Display info about us
    """
    template = "us.html"
    return locals()

@ajax_or_http_response
def peter(request):
    """ Display info about peter
    """
    portfolio = Portfolio.objects.filter(owner="P")
    template = "peter.html"
    return locals()

@ajax_or_http_response
def laura(request):
    """ Display info about laura
    """
    portfolio = Portfolio.objects.filter(owner="L")
    template = "laura.html"
    return locals()

@ajax_or_http_response
def alice(request):
    """ Display info about Alice
    """
    template = "alice.html"
    return locals()

@ajax_or_http_response
def sample_workflow(request):
    """ Display a sample workflow
    """
    template = "sample_workflow.html"
    return locals()

@ajax_or_http_response
def rates(request):
    """ Displays our rates and services
    """
    template = "rates.html"
    return locals()

@ajax_or_http_response
def play(request):
    """ Displays the play page
    """
    template = "play.html"
    return locals()

@ajax_or_http_response
def comic(request, comic_id=None):
    """ Displays the comic
    """
    template = "comic.html"
    comics = Comic.objects.all()
    if not comic_id:
        if comics.count():
            comic_id = comics.latest().id
    if comics.count():
        paginator = Paginator(Comic.objects.all(), 1)
        page = paginator.page(comic_id)
        comic = comics.get(id=comic_id)
    return locals()
