from django.urls import path
from django.contrib import admin
from . import views,cart
urlpatterns = [
    path("products/<int:myid>", views.productView, name="ProductView"),
    path('addproduct',views.addproduct,name='addproduct'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path("search", views.search, name="Search"),
    path("listing/", views.listing, name="listing"),
    path('list/', views.ProductListView.as_view(), name="list"),
    path('viewmyproducts/', views.viewmyproducts, name='viewmyproducts'),
    path("updateproduct/<int:myid>", views.updateproduct, name="updateproduct"),

    path('cart/', cart.mycart, name='mycart'),
    path('addtocart/', cart.addtocart, name='addtocart'),
    path('increaseqty/', cart.increaseqty, name='increaseqty'),
    path('decreaseqty/', cart.decreaseqty, name='decreaseqty'),

]
   