from django.http import HttpResponseRedirect

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
            project.save()
            return HttpResponseRedirect("/work/")
        else:
            errors=form.errors
    else:
        form = ProjectForm()
    return locals()
