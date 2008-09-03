from django.conf.urls.defaults import *
from emlprime.settings import MEDIA_ROOT

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'}),
)

urlpatterns += patterns('',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
 )

urlpatterns += patterns("emlprime.views",
    (r'^work/$', 'detail'),
    (r'^us/$', 'us'),
    (r'^work/create/$', 'confirmation'),
    (r'^project/create/$', 'detail'),
    (r'^play/$', 'play'),
    (r'^play/get_answer_key/$', 'get_answer_key'),
    (r'^work/sample_workflow/$', 'sample_workflow'),
    (r'^work/rates/$', 'rates'),
)
