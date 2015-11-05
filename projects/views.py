from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .serializers import ProjectSerializer

from .models import Project
from .forms import ProjectForm


def projects_home(request):
    CASE_SQL = '''(case
        when status="i" then 1
        when status="f" then 2
        when status="p" then 3
    end)'''

    # projects = Project.objects.extra(select={'order': CASE_SQL}, order_by=['order'])
    projects = Project.objects.order_by('-modified')
    return render(request, "projects_home.html", {'projects': projects})


def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()

            return HttpResponseRedirect(reverse('view_project', args=[project.id]))

    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})


@login_required
def add_participation(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user not in project.participants.all():
        project.participants.add(request.user)
    return HttpResponseRedirect(reverse('view_project', args=[pk]))


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
