from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.vendorLogin,name="vendorLogin"),
    path('account/',views.accountVendor,name="accountVendor"),
    path('documents/upload/',views.documents,name="documents"),
    path('add-products/',views.addProducts,name="addProducts"),
]

