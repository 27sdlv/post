from django import forms
from . import models

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'body','slug', 'banner']   

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body'] 
        labels = {
            'body': ''
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 1, 
                'placeholder': 'Write a comment...',
                'oninput': 'this.style.height = ""; this.style.height = this.scrollHeight + "px"',
                'style': 'overflow: hidden; resize: none;'
            })
        }