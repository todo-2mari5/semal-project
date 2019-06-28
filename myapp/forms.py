from django import forms
from .models import Post, EventInfo


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
