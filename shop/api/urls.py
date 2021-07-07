from django.urls import path
from django.contrib import admin
from . import views,cart
urlpatterns = [

    path('product-api/', views.product_api, name='product-api'),
    path('product-api/<int:id>', views.product_api, name='product-api'),
    path('list/', views.ApiProductListView.as_view(), name="list"),
    path('product-api/<int:id>', views.product_api, name='product-api'),

    path('addtocart/', cart.cart_api, name='cart-api'),
]