from django.db import models
import uuid

class Project(models.Model):
    '''
    Project table
    '''
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    demo_link = models.URLField(max_length=2000, null=True, blank=True)
    source_link = models.URLField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag')
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def __str__(self) -> str:
        '''
        String representation of Project instance
        '''
        return self.title

class Review(models.Model):
    '''
    Review table
    '''
    value_tuple = [
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    ]
    #owner = 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(choices=value_tuple, max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    
    def __str__(self):
        '''
        string representation of a review
        '''
        return self.value

class Tag(models.Model):
    # tag classification for projects
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        '''
        string representation of a tag
        '''
        return self.name
