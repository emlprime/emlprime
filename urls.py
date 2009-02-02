from django.conf.urls.defaults import *
from django.contrib import admin

from emlprime.settings import MEDIA_ROOT
from emlprime.static.models import Project, Blog, Comic, BlogFeed, ComicFeed


admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'}),
    (r'^new_layout/$', 'direct_to_template', {'template': 'index_960.html'}),
)

feeds = {
    'blog' : BlogFeed,
    'comic' : ComicFeed,
}

urlpatterns += patterns('',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^admin/(.*)$', admin.site.root),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),                        
)

latest_comic_id = Comic.objects.latest().id if Comic.objects.count() else 1
urlpatterns += patterns('django.views.generic.list_detail',
    (r'^play/blog/$', 'object_list',{'queryset': Blog.objects.all(), 'template_name': 'blog.html', 'paginate_by': 5, 'page': 1}),
    (r'^play/blog/(?P<page>\d+)', 'object_list',{'queryset': Blog.objects.all(), 'template_name': 'blog.html', 'paginate_by': 5}),
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
    (r'^play/comic/(?P<comic_id>\d+)/$', 'comic'),
    (r'^play/comic/$', 'comic'),
)
