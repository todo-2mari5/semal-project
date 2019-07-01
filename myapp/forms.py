from django import forms
from .models import Post, EventInfo
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'thumb')


class EventForm(forms.ModelForm):

    class Meta:
        model = EventInfo
        fields = ('event_date', 'event_time', 'venue', 'flyer', 'fee', 'registration', 'lang', 'host')
        widgets = {
            'event_date': forms.SelectDateWidget
        }


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        if not 'kyoto-u.ac.jp' in email:
            raise forms.ValidationError("このアドレスは使用できません。京都大学のドメインのものを使用してください")
        else:
            User.objects.filter(email=email, is_active=False).delete()
            return email
