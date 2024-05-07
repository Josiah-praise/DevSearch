from django.contrib import admin
from users.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Skill


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = get_user_model()
    # fieldsets represent the fields that the admin is allowed to
    # display and change
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': 
            ('first_name', 'last_name', 'email', 'social_youtube', 'short_intro',
             'bio', 'location', 'social_linkedin', 'social_github', 'social_twitter',
             'social_website', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Skill)