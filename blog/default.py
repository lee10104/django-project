import .models import *
import .crawler import *

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
