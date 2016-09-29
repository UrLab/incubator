from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .views import (
    ProjectDetailView, ProjectAddView, ProjectEditView,
    projects_home, add_participation, remove_participation,
    add_task, complete_task, uncomplete_task)

urlpatterns = [
    url(r'^$', projects_home, name='projects_home'),
    url(r'^add$', ProjectAddView.as_view(), name='add_project'),
    url(r'^edit/(?P<pk>[0-9]+)$', ProjectEditView.as_view(), name='edit_project'),
    url(r'^(?P<pk>[0-9]+)$', ProjectDetailView.as_view(), name='view_project'),
    url(r'^addtask/(?P<pk>[0-9]+)$', require_POST(add_task), name='add_task'),
    url(r'^complete/(?P<pk>[0-9]+)$', complete_task, name='complete_task'),
    url(r'^uncomplete/(?P<pk>[0-9]+)$', uncomplete_task, name='uncomplete_task'),
    url(r'^participe/(?P<pk>[0-9]+)$', login_required(add_participation), name='project_add_participation'),
    url(r'^noparticipe/(?P<pk>[0-9]+)$', login_required(remove_participation), name='project_remove_participation'),
]
