
from django.urls import path

from user import views

urlpatterns = [
    # 注册
    path('register/', views.register, name='register'),
    # 登录
    path('login/', views.login, name='login'),
    # 报告首页
    path('index/', views.index, name='index'),
    # # 注销
    path('logout/', views.logout, name='logout'),
]