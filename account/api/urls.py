from django.urls import path
from django.contrib import admin
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/',views.userregister,name='register'),
    path('login/',obtain_auth_token,name='login'),
    # path('login/',views.login,name='login'),
    # path('vendorregister',views.vendorregister,name='vendorregistration'),
]