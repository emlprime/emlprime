from django.conf.urls.defaults import *
from django.contrib import admin

from emlprime.settings import MEDIA_ROOT
from emlprime.static.models import Project, Blog, Comic


admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'}),
    (r'^new_layout/$', 'direct_to_template', {'template': 'index_960.html'}),
)

urlpatterns += patterns('',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^admin/(.*)$', admin.site.root),
 )

latest_comic_id = Comic.objects.latest().id if Comic.objects.count() else 1
urlpatterns += patterns('django.views.generic.list_detail',
    (r'^play/comic/(?P<object_id>\d+)/$', 'object_detail',{'queryset': Comic.objects.all(), 'template_name': 'comic.html'}),
    (r'^play/comic/$', 'object_detail',{'queryset': Comic.objects.all(), 'template_name': 'comic.html', 'object_id': latest_comic_id}),
    (r'^play/blog/$', 'object_list',{'queryset': Blog.objects.all(), 'template_name': 'blog.html'}),
)

urlpatterns += patterns("emlprime.views",
    (r'^work/$', 'detail'),
    (r'^us/$', 'us'),
    (r'^us/peter/$', 'peter'),
    (r'^us/laura/$', 'laura'),
    (r'^us/alice/$', 'alice'),
    (r'^work/create/$', 'confirmation'),
    (r'^project/create/$', 'detail'),
    (r'^play/$', 'play'),
    (r'^play/game/$', 'game'),
    (r'^play/get_answer_key/$', 'get_answer_key'),
    (r'^work/sample_workflow/$', 'sample_workflow'),
    (r'^work/rates/$', 'rates'),
)
