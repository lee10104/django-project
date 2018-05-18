from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.contrib.auth.models import User
from .core import *

class Category(models.Model):
    name = models.CharField(max_length=100)

class Picture(models.Model):
    category = models.ForeignKey('Category')
    image = models.ImageField(upload_to=upload_path)
    link = models.TextField(validators=[URLValidator()])

class Novel(models.Model):
    book_code = models.IntegerField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    category = models.ForeignKey('Category') #TODO: Don't combine picture and novel category - fix it later
    cover = models.CharField(max_length=200, validators=[URLValidator()])
    info = models.TextField(blank=True)
    last_update = models.DateTimeField()
    muted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
