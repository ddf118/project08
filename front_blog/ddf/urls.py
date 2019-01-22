from django.urls import path

from ddf import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('share/', views.share, name='share'),
    path('list/', views.list, name='list'),
    path('about/', views.about, name='about'),
    path('gbook/', views.gbook, name='gbook'),
    path('info/', views.info, name='info'),
    path('infopic/', views.infopic, name='infopic'),

    path('', views.index)
]
