from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # test view
    path('', views.UserListView.as_view(), name='user_list'),
    path('detail/<str:pk>', views.users, name='user_detail'),
    path('login', views.UserLogin, name='login'),
    path('logout', views.UserLogout, name='logout'),
    path('register', views.register, name='register'),
    path('account', views.userAccount, name='account'),
    path('edit-account', views.editAccount, name='edit_account'),
]
