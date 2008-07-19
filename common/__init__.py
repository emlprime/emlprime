import re
from datetime import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext, escape
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils import simplejson

def render_ajax_response(context, request):
        context['error_message'] = get_and_delete_messages(request, 'error')
        # remove any non-string items, as they will break the json format
        for key, value in context.items():
                if not isinstance(value, str) and not isinstance(value, list) and not isinstance(value, dict):
                        del context[key]
        json = simplejson.dumps(get_ajax_response(context))
        return HttpResponse(json, mimetype='application/json')

def single_display_session_values(request, context):
        """ fill the context with session values we only wanted to display once

        This is so that we can persist context values just long enough to survive an HttpResponseRedirect
        error messages, status messages, etc.
        """
        context['error_message'] = get_and_delete_messages(request, 'error')
        context['status_message'] = get_and_delete_messages(request, 'status')
        context['focus'] = get_and_delete_focus(request)
        context['id_created'] = get_and_delete_id_created(request)
        return context

def get_and_delete_messages(request, key):
        message_type = "%s_messages" % key
        message_buffer = "".join(['%s' % (message) for message in request.session.get(message_type, [])])
        request.session[message_type] = []
        return message_buffer

def get_and_delete_focus(request):
        focus = request.session.get('focus', '')
        request.session['focus'] = ''
        return focus

def get_and_delete_redirect_url(request):
        redirect_url = request.session.get('redirect_url', '')
        request.session['redirect_url'] = ''
        return redirect_url

def get_and_delete_id_created(request):
        id_created = request.session.get('id_created', '')
        request.session['id_created'] = ''
        return id_created

def set_redirect_url(request, redirect_url):
        """ Use this function to redirect from an ajax response

        ie. redirect_url(request, '/account/')
        """
        request.session['redirect_url'] = redirect_url
        return redirect_url

def highlight_created(request, node_id):
        """ Use this function to highlight a node that has been created or modified

        ie. highlight_created(request, '#category_4')
        """
        request.session['id_created'] = node_id
        return node_id

def status(request, message):
        """ Use this function to display status messages to the user

        ie. status(request, "Your account has been created.")
        """
        return append_message(request.session, 'status', message)

def error(request, message):
        """ Use this function to display generic errors to the user

        ie. error(request, "You cannot delete the default General budget.")
        """
        return append_message(request.session, 'error', message)

def form_error(request, form):
        """ Use this function to display form validation errors to the user

        ie. error(request, "That username is taken.  Please choose another.")
        """
        for name, value in form.errors.items():
                if name == '__all__':
                        name = 'Error'
                error(request, "%s: %s" % (name, value.as_text()))

def append_message(session, key, message):
        message_type = "%s_messages" % key
        messages = session.get(message_type, [])
        if not messages:
                messages = []

        messages.append(str(message))
        session[message_type] = messages
        return messages

def is_ajax(request):
        values = request.POST.copy() if request.method.upper() == "POST" else request.GET.copy()
        if 'is_ajax' in values.keys():
                if values['is_ajax']:
                        return True
        return False

def get_ajax_or_http_redirect(request, url):
        if is_ajax(request):
                if '?' in url:
                        url = url + "&is_ajax=true"
                else:
                        url = url + "?is_ajax=true"
                return url
        return url

def escape_js(value):
        return str(value.replace('\'',''))



