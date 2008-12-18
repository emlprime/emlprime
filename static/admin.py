from django.contrib import admin

from emlprime.static.models import Blog, Comic


class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Blog, BlogAdmin)

class ComicAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comic, ComicAdmin)

