from bs4 import BeautifulSoup
from datetime import datetime
from .models import *
from .core import *
import urllib.parse as urlparse
import requests
from pytz import timezone

# Constants
JOARA_URL = 'http://www.joara.com/'
ROMANCE_URL = 'http://www.joara.com/romancebl/view/book_intro.html?book_code='
NOT_ROMANCE_URL = 'http://www.joara.com/literature/view/book_intro.html?book_code='

def get_soup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def get_romance_dict(book_code):
    soup = get_soup(ROMANCE_URL+str(book_code))
    valid = False
    novel = {
        'valid': valid,
    }
    if not soup.find('em', class_='ico_new'):
        return novel
    else:
        novel['valid'] = True

    try:
        real_category_name = soup.find('select', class_='fe_select').find('option', selected=True)['value']
        real_category = Category.objects.get(name=real_category_name)

        img_info = soup.find('div', class_='img_s').find('img')
        cover = img_info['src']
        title = img_info['title']
        author = remove_indents(soup.find('span', class_='member_nickname').contents[0]).replace(' ', '')
        info_txt = soup.find('div', class_='t_cont_v').get_text(' ', strip=True)
        info = remove_indents(info_txt)

        kst = timezone('Asia/Seoul')
        last_update = kst.localize(datetime.strptime(soup.find('span', class_='date').contents[0], '%Y.%m.%d %H:%M'))

        novel.update({
            'title': title,
            'author': author,
            'category': real_category,
            'cover': cover,
            'info': info,
            'last_update': last_update,
        })
    except:
        return None
    return novel

def get_not_romance_dict(book_code):
    soup = get_soup(NOT_ROMANCE_URL+str(book_code))
    valid = False
    novel = {
        'valid': valid,
    }
    if not soup.find('span', class_='work_tit'):
        return novel
    else:
        novel['valid'] = True

    try:
        real_category_name = soup.find('select', class_='fe_select').find('option', selected=True)['value']
        real_category = Category.objects.get(name=real_category_name)

        title = soup.find('span', class_='work_tit').contents[0].find('a').contents[0]['title']
        author = remove_indents(soup.find('span', class_='member_nickname').contents[0]).replace(' ', '')
        cover = soup.find('p', class_='work_img').find('img')['src']
        info_txt = soup.find('p', class_='work_intro').contents[0]
        info = remove_indents(info_txt)

        kst = timezone('Asia/Seoul')
        last_update = kst.localize(datetime.strptime(soup.find('span', class_='date').contents[0], '%Y.%m.%d %H:%M'))

        novel.update({
            'title': title,
            'author': author,
            'category': real_category,
            'cover': cover,
            'info': info,
            'last_update': last_update,
        })
    except:
        return None
    return novel

def get_novel_dict(category, book_code):
    if category.name == 'rofan':
        novel_dict = get_romance_dict(book_code)
        if not novel_dict:
            return novel_dict
        if not novel_dict['valid']:
            novel_dict = get_not_romance_dict(book_code)
    else:
        novel_dict = get_not_romance_dict(book_code)
        if not novel_dict:
            return novel_dict
        if not novel_dict['valid']:
            novel_dict = get_romance_dict(book_code)

    if not novel_dict:
        return novel_dict
    if not novel_dict['valid']:
        novel_dict = None

    return novel_dict

def save_novel(soup, category):
    icon = soup.find('img', class_='ic_19')
    if icon and icon['title'] != '완결':
        return None

    link = soup.find('a')['href']
    book_code = urlparse.parse_qs(urlparse.urlparse(link).query)['book_code'][0]
    kst = timezone('Asia/Seoul')
    last_update = kst.localize(datetime.strptime(soup.find('span', class_='date').contents[0], '%Y.%m.%d %H:%M'))
    print(book_code)

    try:
        novel = Novel.objects.get(book_code=book_code)
        novel.last_update = last_update
        novel.save()
    except:
        novel_dict = get_novel_dict(category, book_code)
        if not novel_dict:
            return None
        novel = Novel.objects.create(
            book_code=book_code,
            title=novel_dict['title'],
            author=novel_dict['author'],
            category=novel_dict['category'],
            cover=novel_dict['cover'],
            info=novel_dict['info'],
            last_update=last_update,
        )

    return novel

def save_novels(category, page_no):
    soup = get_soup(JOARA_URL+'literature/view/book_list.html?sl_category='+category.name+'&page_no='+str(page_no))
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
