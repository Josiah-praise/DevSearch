from django.db import models
from django.contrib.auth.models import AbstractUser, User
import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model
from .customManagers import DeveloperFilter, CustomManager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.png', null=True, blank=True)
    social_github = models.URLField(null=True, blank=True, max_length=1500)
    social_linkedin = models.URLField(null=True, blank=True, max_length=1500)
    social_twitter = models.URLField(null=True, blank=True, max_length=1500)
    social_website = models.URLField(null=True, blank=True, max_length=1500)
    social_youtube = models.URLField(null=True, blank=True, max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    
    
    # when you use the authenticate function, it takes two values
    # username and password. This is because the USERNAME_FIELD on the
    # AbstractBaseUser is set to "username". If you want to use a different field
    # for authentication, set the field to unique and then alter the USERNAME_FIELD
    # attribute to use that field.
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    object = CustomManager()
    search = DeveloperFilter()

    def __str__(self):
        return self.get_full_name()
    
    def get_absolute_url(self):
        return reverse('users:user_detail', args=(self.id,))
    
    class Meta:
        ordering = ["created_at"]


    
class Skill(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    
    def __str__(self):
        return self.name