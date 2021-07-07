import math
from django.shortcuts import render, redirect

from account.models import BloggerAccount, VendorAccount
from blog.views import viewblog
from shop.models import Product
from .models import Contact
from datetime import date


def index(request):
    allProds = []
    Products=Product.objects.values()

    # for cat in cats:
    #     prod = Products.filter(category=cat).order_by('?')
    #     n = len(prod)
    #     nSlides = n // 4 + math.ceil((n / 4) - (n // 4))
    #     allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'general/index.html',{'products':Products})

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
    return render(request, "general/aboutus.html")

def termsandcondition(request):
    return render(request, "general/terms and conditions.html")

def privacypolicy(request):
    return render(request, "general/privacypolicy.html")

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
