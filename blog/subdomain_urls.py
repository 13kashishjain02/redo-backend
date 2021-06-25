from django.urls import path
from . import views
urlpatterns = [
    path('viewblog', views.viewblog, name='viewblog'),
    path('bloggerblogpost/<int:id>', views.bloggerblogpost, name='bloggerblogpost'),
]
