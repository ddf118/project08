
from django.urls import path

from article import views

urlpatterns = [
    # 文章首页
    path('article/', views.article, name='article'),
    # 增加文章
    path('add_article/', views.add_article, name='add_article'),
    # 编辑文章
    path('edit_article/<int:id>/', views.edit_article, name='edit_article'),
    # 删除文章
    path('del_article/<int:id>/', views.del_article, name='del_article'),
]