from django.urls import path, include

urlpatterns = [
    path('', include('general.subdomain_urls')),
    path('', include('blog.subdomain_urls')),
    path('', include('shop.subdomain_urls')),
    path('', include('account.subdomain_urls')),
    path('', include('payment.subdomain_urls'))
]
