from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic.detail import DetailView

from .serializers import ProjectSerializer

from .models import Project


def projects_home(request):
    MAX_PROJECTS = 10
    context = {
        'max_projects': MAX_PROJECTS,
    }

    context['proposition'] = Project.objects.filter(status='p').order_by('-modified')[:MAX_PROJECTS]
    context['progress'] = Project.objects.filter(status='i').order_by('-modified')[:MAX_PROJECTS]
    context['finished'] = Project.objects.filter(status='f').order_by('-modified')[:MAX_PROJECTS]

    return render(request, "projects_home.html", context)


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
