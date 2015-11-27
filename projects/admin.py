from django.contrib import admin

from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'maintainer', 'progress')
    list_filter = ('status',)
    search_fields = ('title', 'description', 'requirements', 'content')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'completed')
