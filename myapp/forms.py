from django import forms
from .models import Post, EventInfo

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'thumb')
