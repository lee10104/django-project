from bs4 import BeautifulSoup
from datetime import datetime
from .models import *
import urllib.parse as urlparse
import requests
from pytz import timezone

# constants
JOARA_CATE = ['fantasy', 'rofan', 'parody']

def get_soup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def get_soup_joara_category(category, page_no):
    return get_soup('http://www.joara.com/literature/view/book_list.html?sl_category='+category+'&page_no='+str(page_no))

def save_novel(soup, category):
    for_adult = soup.find('img', class_='ic_19')
    if for_adult:
        return None

    link = soup.find('a')['href']
    book_code = urlparse.parse_qs(urlparse.urlparse(link).query)['book_code'][0]
    title = soup.find('p', class_='subject').find('a').contents[0]
    author = soup.find('span', class_='member_nickname').contents[0].replace('\n', '').replace(' ', '')
    cover = soup.find('th').find('img')['src']
    kst = timezone('Asia/Seoul')
    last_update = kst.localize(datetime.strptime(soup.find('span', class_='date').contents[0], '%Y.%m.%d %H:%M'))

    try:
        novel = Novel.objects.get(book_code=book_code)
        novel.last_update = last_update
        novel.save()
    except:
        novel = Novel.objects.create(category=category, book_code=book_code, title=title, author=author, cover=cover, last_update=last_update)

    return novel


def save_novels():
    for cate in JOARA_CATE:
        novels = []
        category = Category.objects.get(name=cate)
        for i in range(1, 5):
            soup = get_soup_joara_category(cate, i)
            try:
                series = soup.find('table', class_='tbl_series2').find_all('tr')
            except:
                series = []
            num = 0
            for piece in series:
                if num % 2 == 0:
                    novel = save_novel(piece, category)
                else:
                    pass
                num += 1
