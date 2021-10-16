from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from projects import views

urlpatterns = [
    path('', views.projects_home, name='projects_home'),
    path('add', views.ProjectAddView.as_view(), name='add_project'),
    path('edit/<int:pk>', views.ProjectEditView.as_view(), name='edit_project'),
    path('<int:pk>', views.ProjectDetailView.as_view(), name='view_project'),
    path('addtask/<int:pk>', require_POST(views.add_task), name='add_task'),
    path('complete/<int:pk>', views.complete_task, name='complete_task'),
    path('uncomplete/<int:pk>', views.uncomplete_task, name='uncomplete_task'),
    path('participe/<int:pk>', login_required(views.add_participation), name='project_add_participation'),
    path('noparticipe/<int:pk>', login_required(views.remove_participation), name='project_remove_participation'),
    path('<int:project_id>/upvote/<int:comment_id>', login_required(views.upvote_comment), name='upvote'),
    path('<int:project_id>/downvote/<int:comment_id>', login_required(views.downvote_comment), name='downvote'),
    path('<int:project_id>/comment/add', login_required(views.add_comment), name='add_comment'),
]
