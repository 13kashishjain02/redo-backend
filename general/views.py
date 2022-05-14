from email import message
from itertools import product
import math
from multiprocessing import context
from traceback import print_tb
from django.shortcuts import render, redirect
from account.models import BloggerAccount, VendorAccount,Subscribe
from blog.views import viewblog
from shop.models import Product,Order
from .models import Contact
from blog.models import Blogs
from datetime import date
from django.contrib import messages
from django.db.models import Q
from shop.models import Product,Variation,Cart

def index(request):
    if request.method == "POST" and 'subscribe' in request.POST:
        email = 'email' in request.POST and request.POST['email']
        if Subscribe.objects.filter(email=email).exists():
            messages.error(request,'You have already subscribed !!')
        else:
            Subscribe.objects.create(
            email = email)
            messages.success(request,'Thanks for subscribing us !!')
    blogs = Blogs.objects.all().first()
    return render(request, 'general/index.html',{'blogs':blogs})

def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        if email==None:
            email = request.user.email
        contact_date = date.today()
        cont = Contact.objects.create(name=name, message=message, subject=subject, email=email,
                                      contact_date=contact_date)
        cont.save()
        # return redirect("../contactus")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return render(request, "general/contact.html")

def aboutus(request):
    return render(request, "general/about.html")

def termsandcondition(request):
    return render(request, "general/text.html")

def privacypolicy(request):
    return render(request, "general/text.html")

def starthere(request):
    return render(request, "general/starthere.html")

def comingsoon(request):
    return render(request, "general/comingsoon.html")

def test(request):
    pass


# ----------------------------------------------------------------------
# exception handlers
# ----------------------------------------------------------------------


def handler404(request, exception):
    return render(request, 'general/404.html', status=404)


def handler500(request, exception):
    return render(request, '500.html', status=500)


def search(request):
    query = request.GET.get('search')
    products = Product.objects.filter(Q(category__icontains=query) | Q(subcategory1__icontains=query) |  Q(subcategory2__icontains=query) | Q(subcategory3__icontains=query))
    product = []
    product_v = []
    for p in products:
        if p.has_variation:
            pass
        else:
            product.append(p)

    for p in products:
        if p.has_variation:
            product_v.append(p)
    
    product_variation = []
    variation = Variation.objects.all()

    for p_v in variation:
        for p in product_v:
            if p_v.product == p:
                product_variation.append(p_v)
    print(product_variation)

    context = {
        'products':product,
        'category':query,
        'products_v':product_variation
    }
    return render(request,'general/search.html',context=context)
