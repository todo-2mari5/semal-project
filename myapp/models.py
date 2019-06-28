from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.

class EventInfo(models.Model):
    host = models.TextField()
    venue = models.CharField(max_length=200, default='Place@url')
    fee = models.CharField(max_length=50, default='Free')
    registration = models.CharField(max_length=50, default='Not required')
    lang = models.CharField(max_length=50, default='English')
    event_date = models.DateField()
    event_time = models.CharField(max_length=50, default='00:00-00:00')
    flyer = models.FileField(upload_to='pdf', validators=[FileExtensionValidator(['pdf', ])],)


    def __str__(self):
        return self.host


class Post(models.Model):
    author = models.ForeignKey('myapp.User',on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    thumb = models.ImageField(upload_to='thumbnail', validators=[FileExtensionValidator(['jpg', 'png',])])
    event = models.OneToOneField(EventInfo, on_delete=models.CASCADE)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

        def __str__(self):
            return self.title


class User(AbstractUser):
    pass
