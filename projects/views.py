from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Project
from .forms import ProjectForm
from django.urls import reverse_lazy


class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    # template_name = 'index.html'
    def get_queryset(self) -> QuerySet[Any]:
        return Project.objects.all().order_by('created')


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    # default template name is app/model_form.html
    # success_url = reverse_lazy("projects:project_list")
    # you don't need to set success url
    # if your model has the method get_absolute_url()
    # which sould return the url for that specific object

class ProjectUpdateView(UpdateView):
    model = Project
    fields = '__all__'
    success_url = reverse_lazy("projects:project_list")

class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("projects:project_list")