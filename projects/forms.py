from django.forms import ModelForm
from .models import Project, Review
from django import forms

class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = [
            'title', 'image', 'description',
            'demo_link', 'source_link', 'tags',
            ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # self.fields['owner'].widget = forms.HiddenInput()
        # self.fields is a dict containg a maping of form field names
        # to form field instances
        # the form field instances have a widget attribute which
        # is also an instance of widget classes from django.forms
        # these widget instances have an attrs attribute which is
        # a dictionary of attribute to value
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm): 
    class Meta:
        model = Review
        fields = ['value', 'body']
        label = {
            'value': 'Upvote or Downvote',
            'body': 'leave a review'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'class': 'input'})
        self.fields['value'].widget.attrs.update({'class': 'input'})