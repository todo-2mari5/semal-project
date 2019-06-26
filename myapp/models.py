from django.db import models
from django.utils import timezone
from djanog.contrib.auth.models import AbstractUser

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.SET_PROTECT,)
    title = models.CharField(max_length=200)
    text = models.TextField()
    venue = models.TextField()
    fee = models.TextField()
    registration = models.TextField()
    language = models.TextField()
    host = models.TextField()
    contact = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    event_date = models.DateTimeField(default=timezone.now)
    flyer = models.ImageField(upload_to='myapp')
    thumb = models.ImageField(upload_to='myapp')



    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class User(AbstractUser):
    pass
