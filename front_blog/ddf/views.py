from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render

from ddf.models import Article, Category


def index(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    counts = Article.objects.values('category_id').annotate(Count('id'))
    # 分页
    page = int(request.GET.get('page', 1))
    pg = Paginator(articles, 5)
    ddf = pg.page(page)
    return render(request, 'index.html', {'articles': articles,
                                          'categories': categories,
                                          'counts': counts,
                                          'ddf': ddf})


def share(request):
    articles = Article.objects.all()
    # 分页
    page = int(request.GET.get('page', 1))
    pg = Paginator(articles, 2)
    ddf = pg.page(page)
    return render(request, 'share.html', {'articles': articles, 'ddf': ddf})


def list(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    counts = Article.objects.values('category_id').annotate(Count('id'))
    # 分页
    page = int(request.GET.get('page', 1))
    pg = Paginator(articles, 5)
    ddf = pg.page(page)
    return render(request, 'list.html', {'articles': articles, 'ddf': ddf, 'categories': categories, 'counts': counts})


def about(request):
    categories = Category.objects.all()
    counts = Article.objects.values('category_id').annotate(Count('id'))
    return render(request, 'about.html', {'categories': categories, 'counts': counts})


def gbook(request):
    categories = Category.objects.all()
    counts = Article.objects.values('category_id').annotate(Count('id'))
    return render(request, 'gbook.html', {'categories': categories, 'counts': counts})


def info(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    counts = Article.objects.values('category_id').annotate(Count('id'))
    return render(request, 'info.html', {'articles': articles, 'categories': categories, 'counts': counts})


def infopic(request):
    categories = Category.objects.all()
    counts = Article.objects.values('category_id').annotate(Count('id'))
    return render(request, 'infopic.html', {'categories': categories, 'counts': counts})