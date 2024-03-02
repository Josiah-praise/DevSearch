from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # test view
    path('', views.users, name='users_info')
]