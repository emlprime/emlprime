from django.conf.urls.defaults import *
from emlprime.settings import MEDIA_ROOT

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'}),
    (r'^us/$', 'direct_to_template', {'template': 'us.html'}),
)

urlpatterns += patterns('',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^work/$', 'emlprime.views.detail'),
)
