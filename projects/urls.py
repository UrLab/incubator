from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import ProjectDetailView, ProjectAddView, ProjectEditView, add_participation, projects_home, remove_participation

urlpatterns = patterns(
    '',
    url(r'^$', projects_home, name='projects_home'),
    url(r'^add$', login_required(ProjectAddView.as_view()), name='add_project'),
    url(r'^edit/(?P<pk>[0-9]+)$', login_required(ProjectEditView.as_view()), name='edit_project'),
    url(r'^(?P<pk>[0-9]+)', ProjectDetailView.as_view(), name='view_project'),
    url(r'^partcipe/(?P<pk>[0-9]+)', login_required(add_participation), name='project_add_participation'),
    url(r'^nopartcipe/(?P<pk>[0-9]+)', login_required(remove_participation), name='project_remove_participation'),
)
