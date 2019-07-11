from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField('タイトル', max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.title