from bs4 import BeautifulSoup
from datetime import datetime
from .models import *
import urllib.parse as urlparse
import requests
from pytz import timezone

# Constants
JOARA_URL = 'http://www.joara.com/'

def get_soup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def get_soup_joara_category(category, page_no):
    return get_soup(JOARA_URL+'literature/view/book_list.html?sl_category='+category+'&page_no='+str(page_no))

def save_novel_info(novel):
    if novel.category.name == 'rofan':
        soup = get_soup(JOARA_URL+'romancebl/view/book_intro.html?book_code='+str(novel.book_code))
    else:
        soup = get_soup(JOARA_URL+'literature/view/book_intro.html?book_code='+str(novel.book_code))
    try:
        info_txt = soup.find('p', class_='work_intro').contents[0]
    except:
        try:
            info_txt = soup.find('div', class_='t_cont_v').get_text(' ', strip=True)
        except:
            info_txt = None
    if info_txt is not None:
        novel.info = info_txt.replace('\t', '').replace('\r', '').replace('\n', '')
        novel.save()

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
        save_novel_info(novel)

    return novel

def save_novels(category, page_no):
    soup = get_soup_joara_category(category, page_no)
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
