from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # test view
    path('', views.UserList, name='user_list'),
    path('detail/<str:pk>', views.user_detail, name='user_detail'),
    path('login', views.UserLogin, name='login'),
    path('logout', views.UserLogout, name='logout'),
    path('register', views.register, name='register'),
    path('account', views.userAccount, name='account'),
    path('edit-account', views.editAccount, name='edit_account'),
    path('add_skill', views.addskill, name='add_skill'),
    path('update_skill/<str:pk>', views.updateskill, name='update_skill'),
    path('delete_skill/<str:pk>', views.delete_skill, name='delete_skill')
]
