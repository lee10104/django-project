from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime, timedelta
from .forms import *
from .crawler import save_novels
import json

def main(request):
    return render(request, 'blog/index.html', {})

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
    except:
        category = None

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
        return HttpResponse(json.dumps(context), 'application/json')

def new_novels(request):
    context = {}
    yesterday = datetime.today() - timedelta(days=1)
    categories = Category.objects.filter(genre=Genre.objects.get(name='novel'))
    new_novels = Novel.objects.filter(last_update__gte=yesterday, muted=False)
    novels_in_cate_list = []
    for category in categories:
        novels_in_cate = {}
        novels_in_cate['name'] = category.kor_name
        novels_in_cate['novel_list'] = new_novels.filter(category=category).order_by('-last_update')
        novels_in_cate_list.append(novels_in_cate)
    context['novels_in_cate_list'] = novels_in_cate_list
    return render(request, 'blog/new_novels.html', context)
