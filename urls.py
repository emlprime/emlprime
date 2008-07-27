from django.conf.urls.defaults import *
from emlprime.settings import MEDIA_ROOT

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'}),
    (r'^us/$', 'direct_to_template', {'template': 'us.html'}),
    (r'^work/sample_workflow/$', 'direct_to_template', {'template': 'sample_workflow.html'}),
)

urlpatterns += patterns('',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^work/$', 'emlprime.views.detail'),
    (r'^work/create/$', 'emlprime.views.confirmation'),
    (r'^project/create/$', 'emlprime.views.detail'),
    (r'^play/$', 'emlprime.views.play'),
)
