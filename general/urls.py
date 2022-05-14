from django.urls import path
from . import views

urlpatterns = [
    # path('', views.starthere, name='starthere'),
    path('', views.index, name='index'),
    path('search/',views.search,name="search"),
]
