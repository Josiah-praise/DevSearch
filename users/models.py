from django.db import models
from django.contrib.auth.models import AbstractUser, User
import uuid


class CustomUser(AbstractUser):
    headline = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=20000, null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    socials = models.OneToOneField('Socials', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Socials(models.Model):
    """
    Stores different social links for a custom user
    """
    instagram = models.URLField(max_length=500, null=True, blank=True)
    facebook = models.URLField(max_length=500, null=True, blank=True)
    github = models.URLField(max_length=500, null=True, blank=True)
    youtube = models.URLField(max_length=500, null=True, blank=True)
    stackoverflow = models.URLField(max_length=500, null=True, blank=True)
    website = models.URLField(max_length=500, null=True, blank=True)