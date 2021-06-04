from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib import messages
from django.utils import timezone
# from datetime import datetime
from actstream import action
from math import ceil
from itertools import groupby

from users.decorators import permission_required
from users.mixins import PermissionRequiredMixin

from .serializers import ProjectSerializer
from .models import Project, Task, Comment
from .forms import ProjectForm, CommentForm


class ProjectAddView(PermissionRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'add_project.html'
    permission_required = 'projects.add_project'

    def get_initial(self):
        return {
            'maintainer': self.request.user,
            'progress': 0,
        }

    def form_valid(self, form):
        ret = super(ProjectAddView, self).form_valid(form)
        action.send(self.request.user, verb='a créé', action_object=self.object)

        return ret


class ProjectEditView(PermissionRequiredMixin, UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = 'add_project.html'
    permission_required = 'projects.change_project'

    def form_valid(self, form):
        ret = super(ProjectEditView, self).form_valid(form)
        action.send(self.request.user, verb='a édité', action_object=self.object)

        return ret


class ProjectDetailView(FormMixin, DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('view_project', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'project': self.object, 'author': self.request.user})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(ProjectDetailView, self).form_valid(form)


def upvote_comment(request, project_id, comment_id):
    user = request.user
    comment = Comment.objects.get(id=comment_id)

    comment.up_vote_user.add(user)
    if user in comment.down_vote_user.all():
        comment.down_vote_user.remove(user)

    return redirect(reverse('view_project', kwargs={'pk': project_id}))


def downvote_comment(request, project_id, comment_id):
    user = request.user
    comment = Comment.objects.get(id=comment_id)

    comment.down_vote_user.add(user)
    if user in comment.up_vote_user.all():
        comment.up_vote_user.remove(user)

    return redirect(reverse('view_project', kwargs={'pk': project_id}))


def clusters_of(seq, size):
    for i in range(int(ceil(len(seq) / size))):
        lower, upper = i * size, (i + 1) * size
        yield seq[lower:upper]


def projects_home(request):
    projects = Project.objects.prefetch_related("participants").select_related("maintainer").order_by('status', '-modified')

    # group the finised and "ants are gone" projets together
    grouper = lambda x: x.status if x.status != "a" else "f"
    groups = {k: list(g) for k, g in groupby(projects, grouper)}
    context = {
        'progress': clusters_of(groups.get('i', []), 4),
        'done': clusters_of(groups.get('f', []), 4),
        'proposition': clusters_of(groups.get('p', []), 4),
    }
    return render(request, "projects_home.html", context)


@permission_required('projects.add_task')
def add_task(request, pk):
    if 'task_name' not in request.POST:
        return HttpResponseBadRequest("Vous n'avez pas donné de nom de tâche")
    project = get_object_or_404(Project, pk=pk)

    task_name = request.POST['task_name'].strip()

    if not task_name or not filter(str.isalpha, task_name):
        messages.add_message(request, messages.ERROR, "Le nom de la tâche est vide")
        return HttpResponseRedirect(reverse('view_project', args=[project.id]))

    task = Task.objects.create(
        project=project,
        name=task_name,
        proposed_by=request.user)

    action.send(request.user, verb='a ajouté la tâche', action_object=task, target=project)

    return HttpResponseRedirect(reverse('view_project', args=[pk]))


@permission_required('projects.change_task')
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed_by = request.user
    task.completed_on = timezone.now()
    task.save()

    action.send(request.user, verb='a fini la tâche', action_object=task, target=task.project)

    return HttpResponseRedirect(reverse('view_project', args=[task.project.id]))


@permission_required('projects.change_task')
def uncomplete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed_by = None
    task.completed_on = None
    task.save()

    action.send(request.user, verb='a ré-ajouté la tâche', action_object=task, target=task.project)

    return HttpResponseRedirect(reverse('view_project', args=[task.project.id]))


def add_participation(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.participants.add(request.user)

    action.send(request.user, verb='participe à', action_object=project)

    return HttpResponseRedirect(reverse('view_project', args=[pk]))


def remove_participation(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.participants.remove(request.user)
    return HttpResponseRedirect(reverse('view_project', args=[pk]))


def add_comment(request, project_id):
    user = request.user
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()

    context = {
        "form": CommentForm(initial={'project': Project.objects.get(id=project_id), 'user': user})
    }
    return render(request, "change_passwd.html", context)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
