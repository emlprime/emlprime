from django.conf.urls.defaults import *
from django.contrib import admin

from emlprime.settings import MEDIA_ROOT
from emlprime.static.models import Project, Blog, Comic, BlogFeed, ComicFeed


admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'}),
)

urlpatterns += patterns('',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^admin/(.*)$', admin.site.root),
)

