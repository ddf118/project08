from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=10, verbose_name='栏目名称', null=False, unique=True)
    alias = models.CharField(max_length=10, verbose_name='栏目别名', null=False, unique=True)
    keywords = models.CharField(max_length=10, null=True, verbose_name='关键字')
    describe = models.CharField(max_length=255, null=True, verbose_name='描述')

    class Meta:
        db_table = 'category'