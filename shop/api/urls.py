from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [

    path('product-api/', views.product_api, name='product-api'),
    path('product-api/<int:id>', views.product_api, name='product-api'),
    path('list/', views.ApiProductListView.as_view(), name="list"),
]