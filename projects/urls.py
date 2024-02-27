from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("list-projects/", views.ProjectListView.as_view(), name='project_list'),
    path("project-detail/<str:pk>/", views.ProjectDetailView.as_view(), name='project_detail'),
    path("create-project/", views.ProjectCreateView.as_view(), name='project_create'),
    path("update-project/<str:pk>", views.ProjectUpdateView.as_view(), name="project_update"),
    path("delete-project/<str:pk>", views.ProjectDeleteView.as_view(), name="project_delete")
]