from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.vendorLogin,name="vendorLogin"),
    path('account/',views.accountVendor,name="accountVendor"),
    path('documents/upload/',views.documents,name="documents"),
    path('add-products/',views.addProducts,name="addProducts"),
    path('add-products/variations/',views.addProductVariation,name="addProductVariation"),
    path('store/add-products/variations/',views.storeVproducts,name="storeVproducts"),
    path('products/',views.products,name="products"),
    path('product/edit/<int:id>/',views.edit_products,name="Edit-product"),
    path('product/variation/edit/<int:id>/',views.edit_product_variation,name="Edit-product-variation"),
    path('orders/',views.orders,name="orders"),
]

