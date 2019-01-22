from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from article.models import Article
from category.models import Category


def category(request):
    """
    栏目展示方法
    """
    if request.method == 'GET':
        # 获取所有的栏目
        categories = Category.objects.all()
        counts = Article.objects.values('category_id').annotate(Count('id'))
        return render(request, 'category.html', {'categories': categories,
                                                 'counts': counts,})


def add_category(request):
    """
    栏目增加方法
    """
    # if request.method == 'GET':
    #     return render(request, 'add-category.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        alias = request.POST.get('alias')
        keywords = request.POST.get('keywords')
        describe = request.POST.get('describe')
        # 使用all()方法进行判断，如果文章标题和内容任何一个参数没有填写，则返回错误信息
        if not all([name, alias]):
            msg = '请填写完整的参数'
            return render(request, 'add-category.html', {'msg': msg})
        # 添加到数据库栏目
        Category.objects.create(name=name,
                                alias=alias,
                                keywords=keywords,
                                describe=describe)
        # 创建文章成功后，跳转到栏目列表页面
        return HttpResponseRedirect(reverse('category:category'))


def edit_category(request, id):
    """
    栏目编辑方法
    """
    if request.method == 'GET':
        category = Category.objects.filter(pk=id).first()
        return render(request, 'edit-category.html', {'category': category})
    if request.method == 'POST':
        # 获取栏目的标题和内容
        name = request.POST.get('name')
        alias = request.POST.get('alias')
        keywords = request.POST.get('keywords')
        describe = request.POST.get('describe')
        # 使用all()方法进行判断，如果栏目标题和内容任何一个参数没有填写，则返回错误信息
        if not all([name, alias]):
            msg = '请填写完整的参数'
            return render(request, 'edit-category.html', {'msg': msg})
        # 编辑栏目
        Category.objects.filter(pk=id).update(name=name,
                                              alias=alias,
                                              keywords=keywords,
                                              describe=describe)
        # 修改栏目成功后，跳转到栏目列表页面
        return HttpResponseRedirect(reverse('category:category'))


def del_category(request, id):
    if request.method == 'GET':
        Category.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('category:category'))
