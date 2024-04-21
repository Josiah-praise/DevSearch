from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
)
from .models import Project
from users.models import CustomUser
from .forms import ProjectForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .utils import paginate, search


def ProjectList(request):
    context = search(request, Project, "projects")
    query_set, _range = paginate(request, 6, context["projects"])
    context["projects"] = query_set
    context["range"] = _range
    return render (request, "projects/project_list.html", context)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("users:account")

    # link the project to the logged-in user
    # form valid is your hook for getting the valid form before saving2
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("users:account")

@login_required
def delete_project(request, pk):
    user = request.user
    if user.project_set.filter(id=pk).exists():
        project = user.project_set.get(id=pk)
        next = request.GET.get('next', '')
        context = {'object': project, 'next': next}
    else:
        return redirect("users:account")

    if request.method == 'POST':
        project.delete()
        messages.success(request, "Delete Sucessful")
        return redirect("users:account")
    return render(request, 'confirm_delete.html', context)


