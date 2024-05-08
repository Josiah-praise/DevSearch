from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectList, name='project_list'),
    path("project-detail/<str:pk>/", views.ProjectDetailView.as_view(), name='project_detail'),
    path("create-project/", views.ProjectCreateView.as_view(), name='project_create'),
    path("update-project/<str:pk>", views.ProjectUpdateView.as_view(), name="project_update"),
    path("delete-project/<str:pk>", views.delete_project, name="project_delete"),
    path("review/<str:pk>", views.review, name='review'),
    path("inbox", views.inbox, name='inbox'),
    path("inbox-detail/<str:pk>", views.inbox_detail, name='inbox_detail'),
    path('send/<str:pk>', views.send_message, name='send_message')
]
