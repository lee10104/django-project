from .models import *
from .crawler import *
import os

# set default db contents
def set_db():
    # create default genre
    picture = Genre.objects.create(name='picture')
    novel = Genre.objects.create(name='novel')

    # create default category - picture
    sakura = Category.objects.create(genre=picture, name='sakura', kor_name='사쿠라')

    # create default category - novel
    rofan = Category.objects.create(genre=novel, name='rofan', kor_name='로맨스 판타지')
    parody = Category.objects.create(genre=novel, name='parody', kor_name='패러디')
    fantasy = Category.objects.create(genre=novel, name='fantasy', kor_name='판타지')

    # save novels
    categories = Category.objects.filter(genre__name='novel')
    for page_no in range(1, 6):
        for category in categories:
            save_novels(category, page_no)

# start celery
def start_celery():
    # start celeryd
    os.system(
        'celery multi start worker1 \
        -A homepage \
        --logfile="$HOME/django-project/logs/celery/%n%I.log" \
        --pidfile="$HOME/django-project/logs/celery/%n.pid"'
    )
    # start celerybeat
    os.system(
        'celery beat -A homepage \
        --pidfile="$HOME/django-project/logs/celery/beat.pid" \
        --detach'
    )

# restart celery
def restart_celery():
    # restart celeryd
    os.system(
        'celery multi restart worker1 \
        -A homepage \
        --logfile="$HOME/django-project/logs/celery/%n%I.log" \
        --pidfile="$HOME/django-project/logs/celery/%n.pid"'
    )

# deploy
def deploy():
    # collectstatic
    os.system('python manage.py collectstatic')
    # restart gunicorn
    os.system('sudo systemctl daemon-reload')
    os.system('sudo systemctl restart gunicorn')
    # restart nginx
    os.system('sudo service restart nginx')
