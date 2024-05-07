from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from . import models


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'bio', 'location', 'profile_image', 'short_intro',
            'social_linkedin', 'social_github', 'social_twitter',
            'social_website', 'social_youtube', 
            )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})

# below is a reminder of what a model field can do
"""
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'password': 'Password'
        }

        help_texts = {
            'password': 'Your password must be at least 8 characters long.'
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

        error_messages = {
            'username': {
                'required': 'Please enter your username.',
                'unique': 'This username is already taken.',
            },
            'email': {
                'required': 'Please enter your email address.',
                'invalid': 'Please enter a valid email address.',
            },
            'password': {
                'required': 'Please enter your password.',
                'min_length': 'Your password must be at least 8 characters long.',
            }
        }
"""

class Addskill(forms.ModelForm):
    class Meta:
        model = models.Skill
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs["class"] = "input"