from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [

    path('product-api/', views.Product_api, name='product-api'),
    path('product-api/<int:id>', views.Product_api, name='product-api'),

]