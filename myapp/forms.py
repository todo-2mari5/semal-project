from django import forms
from .models import Post, EventInfo


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'thumb', 'published_date')


class EventForm(forms.ModelForm):

    class Meta:
        model = EventInfo
        fields = ('host', 'venue', 'event_date', 'start_time')
