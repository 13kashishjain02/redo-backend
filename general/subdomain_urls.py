from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.test, name='test'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('termsandcondition/', views.termsandcondition, name='termsandcondition'),
    path('contactus/', views.contactus, name='contact'),
    path('comingsoon/', views.comingsoon, name='comingsoon'),
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
]
