from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from datetime import datetime
from math import ceil

from .serializers import ProjectSerializer

from .models import Project, Task
from .forms import ProjectForm


class ProjectAddView(CreateView):
    form_class = ProjectForm
    template_name = 'add_project.html'

    def get_initial(self):
        return {
            'maintainer': self.request.user,
            'progress': 0,
        }


class ProjectEditView(UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = 'add_project.html'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'


def clusters_of(seq, size):
    for i in range(int(ceil(len(seq) / size))):
        lower, upper = i * size, (i + 1) * size
        yield seq[lower:upper]


def projects_home(request):
    projects = Project.objects.prefetch_related("participants").select_related("maintainer").order_by('-modified')
    return render(request, "projects_home.html", {
        'projects': clusters_of(projects, 4)
    })


def add_task(request, pk):
    if 'task_name' not in request.POST:
        return HttpResponseBadRequest("Vous n'avez pas donné de nom de tâche")
    project = get_object_or_404(Project, pk=pk)
    Task.objects.create(project=project, name=request.POST['task_name'],
                        proposed_by=request.user)
    project.save()
    return HttpResponseRedirect(reverse('view_project', args=[pk]))


def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed_by = request.user
    task.completed_on = datetime.now()
    task.save()
    task.project.save()
    return HttpResponseRedirect(reverse('view_project', args=[task.project.id]))


def uncomplete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed_by = None
    task.completed_on = None
    task.save()
    task.project.save()
    return HttpResponseRedirect(reverse('view_project', args=[task.project.id]))


def add_participation(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.participants.add(request.user)
    return HttpResponseRedirect(reverse('view_project', args=[pk]))


def remove_participation(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.participants.remove(request.user)
    return HttpResponseRedirect(reverse('view_project', args=[pk]))


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
