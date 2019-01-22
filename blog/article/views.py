from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from article.models import Article
from category.models import Category


def article(request):
    """
    文章展示方法
    """
    if request.method == 'GET':
        # 获取所有的文章
        articles = Article.objects.all()
        page = int(request.GET.get('page', 1))
        pg = Paginator(articles, 2)
        ddf = pg.page(page)
        return render(request, 'article.html',
                      {'articles': articles, 'ddf': ddf})


def add_article(request):
    """
    文章增加方法
    """
    if request.method == 'GET':
        categories = Category.objects.all()
        articles = Article.objects.all()
        return render(request, 'add.html', {'categories': categories, 'articles': articles})
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        keywords = request.POST.get('keywords')
        describe = request.POST.get('describe')
        category_id = request.POST.get('category')
        tags = request.POST.get('tags')
        visibility = request.POST.get('visibility')
        # 使用all()方法进行判断，如果文章标题和内容任何一个参数没有填写，则返回错误信息
        if not all([title, content]):
            msg = '请填写完整的参数'
            return render(request, 'add.html', {'msg': msg})
        # 添加到数据库文章
        Article.objects.create(title=title,
                               content=content,
                               keywords=keywords,
                               describe=describe,
                               category_id=category_id,
                               tags=tags,
                               visibility=visibility)
        # 创建文章成功后，跳转到文章列表页面
        return HttpResponseRedirect(reverse('article:article'))


def edit_article(request, id):
    """
    文章编辑方法
    """
    if request.method == 'GET':
        article = Article.objects.filter(pk=id).first()
        categories = Category.objects.all()
        return render(request, 'edit.html', {'ddf': article, 'categories': categories})
    if request.method == 'POST':
        # 获取文章的标题和内容
        title = request.POST.get('title')
        content = request.POST.get('content')
        keywords = request.POST.get('keywords')
        describe = request.POST.get('describe')
        category_id = request.POST.get('category')
        tags = request.POST.get('tags')
        visibility = request.POST.get('visibility')
        # 使用all()方法进行判断，如果文章标题和内容任何一个参数没有填写，则返回错误信息
        if not all([title, content]):
            msg = '请填写完整的参数'
            return render(request, 'edit.html', {'msg': msg})
        # 编辑文章
        Article.objects.filter(pk=id).update(title=title,
                                             content=content,
                                             keywords=keywords,
                                             describe=describe,
                                             category_id=category_id,
                                             tags=tags,
                                             visibility=visibility)
        # 修改文章成功后，跳转到文章列表页面
        return HttpResponseRedirect(reverse('article:article'))


def del_article(request, id):
    if request.method == 'GET':
        Article.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('article:article'))