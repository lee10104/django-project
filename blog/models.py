from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.contrib.auth.models import User
from .core import *

class Genre(models.Model):
    name = models.CharField(max_length=100)

class Category(models.Model):
    genre = models.ForeignKey('Genre')
    name = models.CharField(max_length=100)
    kor_name = models.CharField(max_length=100)

class Picture(models.Model):
    category = models.ForeignKey('Category')
    image = models.ImageField(upload_to=upload_path)
    link = models.TextField(validators=[URLValidator()])

class Novel(models.Model):
    book_code = models.IntegerField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    category = models.ForeignKey('Category')
    cover = models.CharField(max_length=200, validators=[URLValidator()])
    info = models.TextField(blank=True)
    last_update = models.DateTimeField()
    muted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# set default genre and category
def setting_db():
    # create default genre
    picture = Genre.objects.create(name='picture')
    novel = Genre.objects.create(name='novel')

    # create default category - picture
    sakura = Category.objects.create(genre=picture, name='sakura', kor_name='사쿠라')

    # create default category - novel
    rofan = Category.objects.create(genre=novel, name='rofan', kor_name='로맨스 판타지')
    parody = Category.objects.create(genre=novel, name='parody', kor_name='패러디')
    fantasy = Category.objects.create(genre=novel, name='fantasy', kor_name='판타지')
