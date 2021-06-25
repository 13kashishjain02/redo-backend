from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('addblog/', views.addblog, name='addblog'),
    path('<str:blogname>/viewblog/', views.viewblog, name='viewblog'),
    path('blogpost/<int:id>', views.blogpost, name='blogpost'),
    path('blog/', views.blog, name='blog'),
]
