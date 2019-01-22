import time

from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from article.models import Article
from user.forms import RegisterForm, LoginForm
from user.models import User


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = make_password(form.cleaned_data['password'])
            User.objects.create(username=username,
                                password=password
                                )
            return HttpResponseRedirect(reverse('user:login'))
        else:
            errors = form.errors
            return render(request, 'register.html', {'errors': errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 用户名存在，密码相同
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('user:index'))
        else:
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


def logout(request):
    if request.method == 'GET':
        request.session.flush()
        return HttpResponseRedirect(reverse('user:login'))


def index(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        times = time.asctime(time.localtime(time.time()))
        return render(request, 'index.html', {'articles': articles, 'times': times})

