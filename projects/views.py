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
from .forms import ProjectForm, ReviewForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .utils import paginate, search

@login_required
def ProjectList(request):
    '''
    list all projects
    '''
    context = search(request, Project, "projects")
    query_set, _range = paginate(request, 6, context["projects"])
    context["projects"] = query_set
    context["range"] = _range
    return render (request, "projects/project_list.html", context)


class ProjectDetailView(LoginRequiredMixin, DetailView):
    '''
    show project details
    '''
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        pass the review form as context for rendering
        '''
        context = super().get_context_data(**kwargs)
        if not self.object.review_set.filter(owner=self.request.user).exists():
            context['show_form'] = True
            context['form'] = ReviewForm()
            return context
        context['show_form'] = False
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    '''
    create project
    '''
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("users:account")

    # link the project to the logged-in user
    # form valid is your hook for getting the valid form before saving2
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        '''
        set current user as project owner before saving project
        '''
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    '''
    update project
    '''
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("users:account") # redirect url after project update

@login_required
def delete_project(request, pk):
    '''
    delete project with id 'pk'
    '''
    user = request.user

    # check if project to be deleted belongs to
    # the logged in user
    if user.project_set.filter(id=pk).exists():
        project = user.project_set.get(id=pk)
        # next = request.GET.get('next', '')
        context = {'object': project}
    else:
        messages.error(request, "Project does not exist")
        return redirect("users:account")

    if request.method == 'POST':
        project.delete()
        messages.success(request, "Delete Sucessful")
        return redirect("users:account")
    return render(request, 'confirm_delete.html', context)

def review(request, pk):
    '''
    create review
    '''
    project = Project.objects.get(id=pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.owner = request.user
        review.project = project
        review.save()
        project.do_vote_total_nd_ratio()
        messages.success(request, 'Review created sucessfully')
        return redirect('projects:project_detail', pk)
    else:
        messages.error(request, 'something went wrong')
        return render(
            request, 'projects/project_detail.html',
            {'project': project, 'form': form}
            )
