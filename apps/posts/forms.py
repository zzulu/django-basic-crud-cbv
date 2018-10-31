from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='Comment')

    class Meta:
        model = Comment
        fields = ['content',]
