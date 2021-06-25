from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.userregister,name='register'),
    path('login/',views.userlogin,name='login'),

]
