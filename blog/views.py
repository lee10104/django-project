from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *

def main(request):
    return render(request, 'blog/index.html', {})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        if user is not None and user.check_password(password):
            auth_login(request, user)
            return redirect('main')
        else:
            return HttpResponse('다시 해보세요')
    else:
        if request.user.is_authenticated():
            return render(request, 'blog/index.html', {})
        else:
            return render(request, 'blog/login.html', {})

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

def sakura(request):
    try:
        category = Category.objects.get(name='sakura')
    except:
        category = Category.objects.create(name='sakura')
    pictures = Picture.objects.filter(category=category)
    form = PictureForm()
    context = {
        'category': category,
        'pictures': pictures,
        'form': form,
    }
    return render(request, 'blog/sakura.html', context)

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
                return redirect('sakura')

@login_required
def delete_picture(request):
    return redirect('sakura')
