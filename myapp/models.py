from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class EventInfo(models.Model):
    host = models.TextField()
    venue = models.CharField(max_length=200)
    fee = models.CharField(max_length=200)
    registration = models.CharField(max_length=200)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    flyer = models.ImageField(upload_to='myapp')


    def __str__(self):
        return self.host


class Post(models.Model):
    author = models.ForeignKey('myapp.User',on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    thumb = models.ImageField(upload_to='myapp')
    event = models.OneToOneField(EventInfo, on_delete=models.CASCADE)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

        def __str__(self):
            return self.title


class User(AbstractUser):
    pass
