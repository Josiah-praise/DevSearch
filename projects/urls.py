from django.urls import path
from .views import Project_Detail, Project_List

app_name = "projects"

urlpatterns = [
    path("list/", Project_List.as_view(), name='project_list'),
    path("detail/<str:pk>/", Project_Detail.as_view(), name='project_detail')
]
