from django.contrib import admin

from emlprime.static.models import Blog, Comic, Project


class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Blog, BlogAdmin)

class ComicAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comic, ComicAdmin)

class ProjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Project, ProjectAdmin)

