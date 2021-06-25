from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', 'redopact.urls', name='www'),
    # host(r'[a-z]+', settings.ROOT_URLCONF, name='admin'),
    host(r'elpizo', 'redopact.urls', name='elpizo'),
    host(r'[a-z]+', 'redopact.subdomain_urls', name='subdomain'),
)
