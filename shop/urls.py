from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [

    path('cart_add/<int:id>', views.cart_add, name='cart_add'),
    path('item_clear/<int:id>', views.item_clear, name='item_clear'),
    path('item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart-detail/',views.cart_detail,name='cart_detail'),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path('addproduct',views.addproduct,name='addproduct'),
    path('placeorder',views.placeorder,name='placeorder'),
    path("search", views.search, name="Search"),
    path('viewmyproducts/', views.viewmyproducts, name='viewmyproducts'),
    path("updateproduct/<int:myid>", views.updateproduct, name="updateproduct"),
]
   