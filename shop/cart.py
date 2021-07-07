from shop.models import Product, SubCategory2,Cart
from django.shortcuts import render
from account.models import VendorAccount
from django.http import HttpResponseRedirect, HttpResponse

def add_to_cart(request):
    pass