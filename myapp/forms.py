from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    file = forms.FileField(
        label='',
        required=False
    )

    class Meta:
        model = Post
        fields = ('title', 'text', 'image')
