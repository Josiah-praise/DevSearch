from django.db import models
from django.contrib.auth.models import AbstractUser, User
import uuid


class CustomUser(AbstractUser):
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

""" class Socials(models.Model):

    Stores different social links for a custom user


    class Meta:
        verbose_name = 'Social' # singular model name
        verbose_name_plural = 'Socials' # plural model name

    instagram = models.URLField(max_length=500, null=True, blank=True)
    facebook = models.URLField(max_length=500, null=True, blank=True)
    github = models.URLField(max_length=500, null=True, blank=True)
    youtube = models.URLField(max_length=500, null=True, blank=True)
    stackoverflow = models.URLField(max_length=500, null=True, blank=True)
    website = models.URLField(max_length=500, null=True, blank=True) """
    
class Skill(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    
    def __str__(self):
        return self.name