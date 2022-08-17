from django.db import models

# Create your models here.
class Feed(models.Model):
    content = models.TextField()
    image = models.TextField()
    email = models.EmailField(default='')
    like_count = models.IntegerField()
