from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext

from emlprime.common import is_ajax, single_display_session_values

AJAX_KEYS = ['ids_to_replace', 'error_message', 'status_message', 'id_created', 'id_deleted', 'focus', 'redirect_url']

def ajax_or_http_response(view):
    """ Determine if this is an ajax request or normal HTTP.  Respond appropriately.
    """
    def _handle_response(request, *args, **kwargs):
        result = view(request, *args, **kwargs)
        # if this is a redirect, just pass it through
        if not isinstance(result, dict):
            return result
        context = single_display_session_values(request, result)
        if is_ajax(request):
            json = simplejson.dumps(get_ajax_response(result))
            return HttpResponse(json, mimetype='application/json')

        try:
            template = result.pop('template')
        except KeyError:
            raise KeyError("You forgot to specify a template in the context returned by your view")

        # put the ids_to_replace in the current context
        if result.has_key('ids_to_replace'):
            ids_to_replace = result.pop('ids_to_replace')
            context.update(ids_to_replace)
            
        # provide the current page's url for navigation links
        context["current_url"] = request.META["PATH_INFO"] if request.META["PATH_INFO"] else "/"
        return render_to_response(template, context, context_instance=RequestContext(request))

    return _handle_response

def get_ajax_response(context):
    """ get_ajax_response returns a hash containing ajax parameters

    parameter replace contains a hash of HTML DOM ids to HTML to be replaced
    per ID.

    the form of the output is:
    {'ids_to_replace': <hash of HTML DOM IDs to replace from id to html>,
    'error_message': <error message to display>,
    'status_message': <status message to display,
    }
    """
    # clean the ids to replace, making sure they don't have javascript in them for security
    if context.has_key('ids_to_replace'):
        context['ids_to_replace'] = dict([(key, escape_js(value)) for key, value in context['ids_to_replace'].items()])

    # list the keys we expect to get back for an ajax response
    ajax_context = {}
    for key in AJAX_KEYS:
        # determine whether the default value should be a string or a dictionary
        default_value = {} if key == 'ids_to_replace' else ''
        value = context.get(key, default_value)
        # if the value is legal json, add it to the dictionary
        if isinstance(value, (str,dict)):
            ajax_context[key] = value

    return ajax_context


def escape_js(value):
        return str(value.replace('\'',''))
