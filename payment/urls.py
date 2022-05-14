from . import views
from django.conf.urls import include, url
from django.urls import path

urlpatterns = [
    path('payucheckout/<str:amount>', views.payucheckout, name='payucheckout'),
    path('payusuccess/', views.payusuccess, name='payusuccess'),
    path('payufailure/', views.payufailure, name='payufailure'),
    path('payusubscription/', views.payusubscription, name='payusubscription'),

    path('paytmcheckout/', views.paytmcheckout, name='paytmcheckout'),
    path('paytmhandlerequest/', views.paytmhandlerequest, name='paytmhandlerequest')
]