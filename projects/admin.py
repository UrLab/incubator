from django.contrib import admin

from .models import Project, Task, Comment


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'maintainer', 'progress')
    list_filter = ('status',)
    search_fields = ('title', 'short_description', 'dependencies__title', 'content')

    filter_horizontal = ('participants', 'dependencies')
    inlines = (TaskInline,)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'completed')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'author', 'up_vote')
