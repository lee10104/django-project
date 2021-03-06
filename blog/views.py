from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from datetime import datetime, timedelta
from .forms import *
from .crawler import save_novels

def main(request):
    twitter_user_ids = ['lee10104_', 'soseol_reader', 'LED_Galaxy']
    twitter_users = []
    for twitter_user in twitter_user_ids:
        response = get_response_from_twitter_api('users/show.json', {'screen_name': twitter_user})
        profile_image = 'https://abs.twimg.com/sticky/default_profile_images/default_profile.png'
        if response:
            if response['status'] == '200':
                user_id = response['data']['screen_name']
                user_name = response['data']['name']
                description = response['data']['description']
                profile_image = response['data']['profile_image_url'].replace('_normal', '')
                twitter_users.append({
                    'user_id': user_id,
                    'user_name': user_name,
                    'description': description,
                    'profile_image': profile_image,
                })

    block = 12 // len(twitter_users)
    return render(request, 'blog/index.html', {'twitter_users': twitter_users, 'block': block})

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, password)
            auth_login(request, user)
            return redirect('main')
    else:
        form = UserForm()
        return render(request, 'blog/signup.html', {'form': form})

def album(request, cate_name):
    try:
        category = Category.objects.get(genre=Genre.objects.get(name='picture'), name=cate_name)
    except Category.DoesNotExist:
        raise Http404()

    pictures = Picture.objects.filter(category=category)
    form = PictureForm()
    context = {
            'category': category,
            'pictures': pictures,
            'form': form,
    }
    return render(request, 'blog/album.html', context)

@login_required
def add_picture(request):
    if request.method == 'POST':
        category = Category.objects.get(name=request.POST.get('category'))
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            link = form.cleaned_data['link']
            image = form.cleaned_data['image']
            if link and image:
                return HttpResponse("하나만 넣으세요")
            elif not link and not image:
                return HttpResponse("하나라도 넣으세요")
            else:
                obj = form.save(commit=False)
                obj.category = category
                obj.save()
                return redirect('album', category.name)
        else:
            return HttpResponse("잘못된 입력입니다.")

def delete_picture(request):
    if request.method == 'POST':
        context = {}
        success = False
        if request.user.is_authenticated():
            try:
                picture = Picture.objects.get(id=request.POST.get('picture_id'))
            except:
                picture = None
            if picture:
                picture.delete()
                success = True
                message = '삭제되었습니다.'
            else:
                message = '잘못된 사진입니다.'
        else:
            message = '먼저 로그인 해주세요.'
        context['success'] = success
        context['message'] = message
        return send_http_response(context)

def new_novels(request, cate_name):
    context = {}
    yesterday = datetime.today() - timedelta(days=1)
    try:
        category = Category.objects.get(genre__name='novel', name=cate_name)
    except Category.DoesNotExist:
        raise Http404()
    new_novels = Novel.objects.filter(category__name=cate_name)

    name = category.kor_name
    novels = new_novels.filter(muted=False, last_update__gte=yesterday).order_by('-last_update')

    paginator = Paginator(novels, 15)
    page_no = request.GET.get('page_no')
    if page_no:
        page_no = int(page_no)
    else:
        page_no = 1
    novel_list = paginator.page(page_no)

    context['name'] = name
    context['novel_list'] = novel_list
    context['categories'] = Category.objects.filter(genre__name='novel')
    return render(request, 'blog/new_novels.html', context)

def mute_novel(request):
    if request.method == 'POST':
        context = {}
        success = False
        book_code = request.POST.get('book_code')
        if request.user.is_authenticated():
            try:
                novel = Novel.objects.get(book_code=book_code)
                novel.mute()
                success = True
                message = '뮤트되었습니다.'
            except:
                message = '해당 소설을 찾을 수 없습니다.'
        else:
            message = '먼저 로그인 해주세요.'
        context['success'] = success
        context['message'] = message
        return send_http_response(context)
