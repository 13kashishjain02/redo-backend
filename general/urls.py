from django.urls import path
from . import views

urlpatterns = [
    # path('', views.starthere, name='starthere'),
    path('', views.index, name='index'),
    path('contactus/', views.contactus, name='contact'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('termsandcondition/', views.termsandcondition, name='termsandcondition'),
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
    path('test/', views.test, name='test'),
    path('comingsoon/', views.comingsoon, name='comingsoon'),
]
