from django.urls import path
from django.contrib import admin
from . import views,cart
from PayTm.views import payment,handle_response,order_success
urlpatterns = [
    # path("product/<int:myid>", views.productView, name="ProductView"),

    path('checkout/cart/',views.cart,name="cart"),
    path('checkout/address/',views.address,name="address"),
    path("checkout/payment/", views.payment, name="payment"),
    path('products/<str:category>/',views.products,name="products"),
    path('products/<str:category>/<str:subcategory1>/',views.products,name="products"),
    path('products/<str:category>/<str:subcategory1>/<str:subcategory2>/',views.products,name="products"),
    path('products/<str:category>/<str:subcategory1>/<str:subcategory2>/<str:subcategory3>/',views.products,name="products"),
    path('<int:id>/buy/',views.productDetails,name="products-details"),
    path('variation/<int:id>/buy/',views.productDetailsVariation,name="products-details-variation"),
    path('change-quantity/<int:id>/',views.change_quantity,name="products-change-quantity"),
    path('remove-product/<int:id>/',views.remove_product,name="remove-product"),
    path('move-to-cart/<int:id>/',views.move_to_cart,name="move-to-cart"),
    path('variation/<int:id>/add-to-cart/',views.productDetailsVariationCart,name="add-to-cart-variation"),
    path('change-quantity-variation/<int:id>/',views.change_quantity_variation,name="products-change-quantity-variation"),
    path('move-to-wishlist/variation/<int:id>/',views.move_to_wishlist_variation,name="move-to-wishlist-variation"),
    path('payment/',payment,name="payment"),
    path('response/',handle_response,name="handle_response"),
    path('order-success/',order_success,name="order_success"),
    path('apply-coupon/',views.apply_coupon,name="apply_coupon"),
    path('remove-coupon/',views.remove_coupon,name="remove_coupon"),
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

    # path('cart/', cart.mycart, name='mycart'),
    # path('addtocart/', cart.addtocart, name='addtocart'),
    # path('increaseqty/', cart.increaseqty, name='increaseqty'),
    # path('decreaseqty/', cart.decreaseqty, name='decreaseqty'),

    path('maintenance/', views.maintenance, name='maintenance'),

]
   