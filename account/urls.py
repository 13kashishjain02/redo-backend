from django.urls import path, include
from django.contrib import admin
from . import views
urlpatterns = [
    path('register/',views.userregister,name='register'),
    path('login/',views.userlogin,name='login'),
    path('vendorregister/',views.vendorregister,name='vendorregistration'),
    path('bloggerregister',views.bloggerregister,name='bloggerregister'),
    path('logout/',views.logoutuser,name='logout'),
    path('account/',views.account_view,name='account'),
    path('choosevendortemplate/',views.choosevendortemplate,name='choosevendortemplate'),
    path('customise-vendor-template/',views.customise_vendor_template,name='customise_vendor_template'),
    path('choosebloggertemplate/',views.choosebloggertemplate,name='choosebloggertemplate'),
    path('customise-blogger-template/',views.customise_blogger_template,name='customise_blogger_template'),
    path('changepassword/',views.changepassword,name='changepassword'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('handlesubscription/',views.handlesubscription,name='handlesubscription'),
    path('subscription/',views.subscription,name='subscription'),
    path('check/',views.check,name='check'),
    path('otpemail/<str:remail>',views.otpemail,name='otpemail'),
    path('otpemail/',views.otpemail,name='otpemail'),

    path('social-auth/', include('social_django.urls', namespace="social")),
]

