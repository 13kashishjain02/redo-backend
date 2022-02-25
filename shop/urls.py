from django.urls import path
from django.contrib import admin
from . import views,cart
urlpatterns = [
    # path("product/<int:myid>", views.productView, name="ProductView"),

    path('checkout/cart/',views.cart,name="cart"),
    path('checkout/address/',views.address,name="address"),
    path("checkout/payment/", views.payment, name="payment"),
    path('products/<slug:category>/',views.products,name="products"),








    path("<slug:slug>!/", views.productView, name="ProductView"),
    path('dashboard',views.dashboard,name='dashboard'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('addvariation',views.addvariation,name='addvariation'),
    path('viewmyproducts/', views.viewmyproducts, name='viewmyproducts'),
    path("updateproduct/<int:myid>", views.updateproduct, name="updateproduct"),
    path("listing/", views.listing, name="listing"),

    path('placeorder/',views.placeorder,name='placeorder'),
    path('myorders/', views.myorders, name='myorders'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('vendororders/', views.vendororders, name='vendororders'),

    path('cart/', cart.mycart, name='mycart'),
    path('addtocart/', cart.addtocart, name='addtocart'),
    path('increaseqty/', cart.increaseqty, name='increaseqty'),
    path('decreaseqty/', cart.decreaseqty, name='decreaseqty'),

    path('maintenance/', views.maintenance, name='maintenance'),

]
   