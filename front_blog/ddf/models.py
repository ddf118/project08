from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=10, verbose_name='栏目名称', null=False, unique=True)
    alias = models.CharField(max_length=10, verbose_name='栏目别名', null=False, unique=True)
    keywords = models.CharField(max_length=10, null=True, verbose_name='关键字')
    describe = models.CharField(max_length=255, null=True, verbose_name='描述')

    class Meta:
        db_table = 'category'


class Article(models.Model):
    title = models.CharField(max_length=10, verbose_name='标题', null=False, unique=True)
    content = models.TextField()
    keywords = models.CharField(max_length=10, null=True, verbose_name='关键字')
    describe = models.CharField(max_length=255, null=True, verbose_name='描述')
    category = models.ForeignKey(Category, verbose_name='栏目', on_delete=models.CASCADE)
    tags = models.CharField(max_length=998, null=True, verbose_name='标签')
    visibility = models.BooleanField(default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='时间', null=True)

    class Meta:
        db_table = 'article'



