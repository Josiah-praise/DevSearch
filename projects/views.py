from typing import Any
from django.db.models.query import QuerySet
# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Project


class Project_List(ListView):
    model = Project
    context_object_name = 'projects'
    def get_queryset(self) -> QuerySet[Any]:
        return Project.objects.all().order_by('created')  


class Project_Detail(DetailView):
    model = Project
    context_object_name = 'project'
