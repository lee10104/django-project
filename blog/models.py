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
