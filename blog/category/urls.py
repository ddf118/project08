
from django.urls import path

from category import views

urlpatterns = [
    # 栏目首页
    path('category/', views.category, name='category'),
    # # 增加栏目
    path('add_category/', views.add_category, name='add_category'),
    # # 编辑栏目
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    # # 删除栏目
    path('del_category/<int:id>/', views.del_category, name='del_category'),
]