from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .serializers import ProjectSerializer

from .models import Project
from .forms import ProjectForm


class ProjectAddView(CreateView):
    form_class = ProjectForm
    template_name = 'add_project.html'


class ProjectEditView(UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = 'add_project.html'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'


def projects_home(request):
    projects = Project.objects.order_by('-modified')
    return render(request, "projects_home.html", {'projects': projects})


@login_required
def add_participation(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user not in project.participants.all():
        project.participants.add(request.user)
    return HttpResponseRedirect(reverse('view_project', args=[pk]))


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
