from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    file = forms.FileField(required=False)
    file = forms.FileField(
        label='',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Post
        fields = ('title', 'text', 'image')
