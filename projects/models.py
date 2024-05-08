from django.db import models
import uuid
from users.models import CustomUser
from django.urls import reverse
from .customManagers import ProjectFilter
from django.db.models import Manager

class Project(models.Model):
    '''
    Project model
    '''
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    demo_link = models.URLField(max_length=2000, null=True, blank=True)
    source_link = models.URLField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag')
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to= 'project_photos', default='default.png', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    objects = Manager()
    search = ProjectFilter()

    def __str__(self) -> str:
        return str(self.title)

    def get_absolute_url(self):
        '''
        returns the url for a project instance
        '''
        return reverse("projects:project_detail", kwargs={"pk": self.id})

    def do_vote_total_nd_ratio(self):
        '''
        calculate project vote ratio and vote total
        '''
        self.vote_total = self.review_set.all().count()
        positive_votes = self.review_set.filter(value='up').count()
        self.vote_ratio = (positive_votes/self.vote_total) * 100
        self.save()

    class Meta:
        ordering = ["-vote_total", "-vote_ratio", "title"]

class Review(models.Model):
    '''
    Review model
    '''
    votes = [
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    ]
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(choices=votes, max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        unique_together = [['owner', 'project']]


class Tag(models.Model):
    '''
    Tag model
    '''
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return str(self.name)

class Inbox(models.Model):
    '''
    Inbox model
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='recipient', null=True)
    is_read = models.BooleanField(default=False)
    body = models.TextField()
    title = models.CharField(max_length=500)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ["is_read", "-sent_at"]
