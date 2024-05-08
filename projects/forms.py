from django.forms import ModelForm
from .models import Project, Review, Inbox
from django import forms

class ProjectForm(ModelForm):
    '''
    Project model form
    '''
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
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    '''
    Review model form
    '''
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

class InboxForm(forms.ModelForm):
    '''
    Inbox model form
    '''
    class Meta:
        model = Inbox
        fields = ['title', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        self.fields['body'].widget.attrs.update({'class': 'input'})
        self.fields['title'].widget.attrs.update({'class': 'input'})
