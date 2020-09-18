from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .views import (
    ProjectDetailView, ProjectAddView, ProjectEditView,
    projects_home, add_participation, remove_participation,
    add_task, complete_task, uncomplete_task)

urlpatterns = [
    path('', projects_home, name='projects_home'),
    path('add', ProjectAddView.as_view(), name='add_project'),
    path('edit/<int:pk>', ProjectEditView.as_view(), name='edit_project'),
    path('<int:pk>', ProjectDetailView.as_view(), name='view_project'),
    path('addtask/<int:pk>', require_POST(add_task), name='add_task'),
    path('complete/<int:pk>', complete_task, name='complete_task'),
    path('uncomplete/<int:pk>', uncomplete_task, name='uncomplete_task'),
    path('participe/<int:pk>', login_required(add_participation), name='project_add_participation'),
    path('noparticipe/<int:pk>', login_required(remove_participation), name='project_remove_participation'),
]
