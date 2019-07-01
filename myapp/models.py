from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.

class Post(models.Model):
    """投稿のデータ"""
    author = models.ForeignKey('myapp.User',on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    """イベントの詳細データ"""
    host = models.TextField(default='host:hostname\ncontact:e-mail')
    venue = models.CharField(max_length=200, default='Place@url')
    fee = models.CharField(max_length=50, default='Free')
    registration = models.CharField(max_length=50, default='Not required')
    lang = models.CharField(max_length=50, default='English')
    event_time = models.CharField(max_length=50, default='00:00-00:00')
    event_date = models.DateField()
    """画像、pdfデータ"""
    thumb = models.ImageField(upload_to='thumbnail', validators=[FileExtensionValidator(['jpg', 'png',])])
    flyer = models.FileField(upload_to='pdf', validators=[FileExtensionValidator(['pdf', ])],)

    def link_maker(self):
        if '@' in self.venue:
            link = self.venue.split('@')
            return link
        else:
            return False

    def __str__(self):
            return self.title


class User(AbstractUser):
    pass
