from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Project
from .forms import ProjectForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    # template_name = 'index.html'
    def get_queryset(self) -> QuerySet[Any]:
        return Project.objects.all().order_by('-created')


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    
    # link the project to the logged-in user
    # form valid is your hook for getting the valid form before saving2
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    # 
    """ def get_form_kwargs(self) -> dict[str, Any]:
        kwargs =  super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs """
    
    # populates your form with some initial values
    """ def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial """
    # default template name is app/model_form.html
    # success_url = reverse_lazy("projects:project_list")
    # you don't need to set success url
    # if your model has the method get_absolute_url()
    # which sould return the url for that specific object

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("projects:project_list")

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