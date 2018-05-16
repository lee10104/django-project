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

def sakura(request):
    return render(request, 'blog/sakura.html', {})
