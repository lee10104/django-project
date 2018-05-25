from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .crawler import save_novels
from .models import *

@shared_task
def joara_crawler():
    categories = Category.objects.filter(genre__name='novel')
    for category in categories:
        for page_no in range(1, 6):
            save_novels(category, page_no)
