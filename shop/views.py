from django.shortcuts import render, redirect
from .models import Product, Order, Cart
from account.models import VendorAccount
from django.contrib.auth.decorators import login_required
from datetime import date
import math
from .forms import AddproductForm
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum2
from twilio.rest import Client
from django.core.paginator import Paginator
from django.views.generic import ListView
import re

MERCHANT_KEY = 'Ujzdeai9L@l%#6!o';
username = ""
orderid = ""

# ----------------------------------------------------------
# static methods
# ----------------------------------------------------------

def getvendor(email):
    vendor = VendorAccount.objects.get(email=email)
    return vendor


def getvendorbyshopname(shop_name):
    vendor = VendorAccount.objects.get(shop_name=shop_name)
    return vendor


def convertstrtolist(x):
    x = str(x)
    bad_chars = ['"', ']', '[', "'", ',']

    for i in bad_chars:
        x = x.replace(i, '')

    x = list(x.split(" "))
    return x


def olist(username):
    orders_temp = Cart.objects.filter(username=username)
    orders = orders_temp.values()
    a = []
    total = 0
    print(orders)
    for i in orders:
        print("hello world",i["product_id"])
        prod = Product.objects.get(id=i["product_id"])
        i["price"] = prod.price
        i["original_price"] = prod.original_price
        i["discount"] = prod.discount
        i["image"] = prod.image
        i["name"] = prod.name
        i["vendor"] = prod.vendor.shop_name
        i["ptotal"] = i["price"] * i["qty"]
        total = total + i["ptotal"]
        a.append(i)

    a.reverse()
    return (a, total)

# --------------------------------------------------------------
# general views
# --------------------------------------------------------------
def myorders(request):
    data = Order.objects.get(user=request.user)
    # previous_order=order.previous_order
    counter=0
    # print(data)
    # for i in data:
    #     product = Product.objects.get(id=i["product_id"])
    #     data[counter]["mrp"] = product.mrp
    #     data[counter]["special_price"] = product.special_price
    #     data[counter]["our_price"] = product.our_price
    #     data[counter]["name"] = product.name
    #     data[counter]["image"] = product.image
    #     data[counter]["discount"] = math.floor(100 - (product.special_price / product.mrp) * 100)
    #     counter+=1

    return render(request, 'shop/myorder.html',{"order":data})


def productView(request, slug):
    # Fetch the product using the id
    product = Product.objects.get(slug=slug)

        # i.size = convertstrtolist(i.size)
    if product.color:
        product.color = re.split('; | ,|, |,| |\n', product.color)
    if product.size:
        product.size = re.split('; | ,|, |,| |\n', product.size)

    return render(request, 'shop/product page.html', {'product': product})

@login_required(login_url="../login")
def placeorder(request):
    if request.method == 'POST':
        username = request.user
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        address = request.POST['address']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zip']
        landmark = request.POST['landmark']
        contact_number = request.POST['contact_number']
        order_list = Cart.objects.get(user=username).cartdata
        total=60 #60 rupees for delivery
        counter = 0
        for i in order_list:
            product=Product.objects.get(id=i["product_id"])
            order_list[counter]["mrp"]=product.mrp
            order_list[counter]["special_price"] = product.special_price
            order_list[counter]["our_price"] = product.our_price
            order_list[counter]["name"] = product.name
            order_list[counter]["status"] = "order placed"
            order_list[counter]["image"] = str(product.image)
            order_list[counter]["vendor_email"] = product.vendor.email
            if product.our_price:
                total = total + product.our_price
            elif product.special_price:
                total = total + product.special_price
            else :
                total = total + product.mrp

            counter+=1

        c_order = Order.objects.create(user=username, order_list=order_list, zipcode=zipcode,
                                       address=address, address2=address2, contact_number=contact_number,
                                       landmark=landmark,city=city,state=state, total=total)
        c_order.save()
        global orderid
        orderid = str(c_order.id)
        # return redirect('../paytmcheckout')
        url = '../payucheckout/' + str(total)
        return redirect(url)
    else:
        return render(request, 'shop/placeorder.html')

# ---------------------------------------------------------------------
# vendor related functions
# ---------------------------------------------------------------------
def dashboard(request):
    return render(request, 'shop/dashboard.html')

def addproduct(request):
    global msg
    chartnum = ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "26", "28", "30", "32", "34", "36", "38", "40",
                "42", "44", "46", "48", "50", "52", "54", "56", "58", "60"]
    chartletter = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]
    if request.user.is_Vendor:
        if request.method == 'POST':
            form = AddproductForm(request.POST, request.FILES)
            if form.is_valid():
                desc = form.cleaned_data['desc']
            print("content:",desc)

            name = request.POST['name']
            vendor = getvendor(request.user.email)
            size = request.POST.getlist('size')
            brand = request.POST['brand']
            tags = request.POST.get('tags')
            category = request.POST['category']
            subcategory = request.POST['subcategory']
            product_for = request.POST.get('product_for')
            discount = request.POST['discount']
            price = request.POST['selling_price']
            stock = request.POST['stock']
            original_price = float(request.POST['price'])
            delivery_charge = request.POST['delivery_charge']
            # desc = request.POST.get('desc', 'Description not available')
            pub_date = date.today()
            myfile = request.FILES['myfile']
            myfile2 = request.FILES.get('myfile2')
            myfile3 = request.FILES.get('myfile3')
            msg = ""
            if product_for == None:
                product_for = "general"

            if price == "":
                price = original_price
                if discount != "":
                    price = price * ((100.00 - float(discount)) / 100.00)
            else:
                price = float(price)

            if discount == "":
                discount = 100 - math.ceil((price / original_price) * 100)

            import random
            # for i in range(4):
            #     name=random.choice(['Jeans', 'Tshirt', 'Skirt', 'Shoes', 'Pant', 'Shirt'])+" Test Product " + str(i)
            #     # vendor = getvendor(random.choice(['jain@jain.com', 'jainshivam100@gmail.com', 'kashish.iitdelhi@gmail.com']))
            #     vendor = getvendor('kashish.iitdelhi@gmail.com')
            #     category = random.choice(['category1', 'category2', 'category3', ])
            #     product_for=random.choice(['men', 'women', 'boys', 'girls', 'kids', 'general'])
            #     price = random.randint(300, 900)
            #     original_price = price
            #     desc = "Heading 1:IT is a TESTING product made for for testing the compatibility of website with " \
            #            "different vendors and their products.Heading 2:This product is not for sale.Heading 3:The " \
            #            "prices mentioned for this product does not hold any value. " + "best " + name +" in "+category
            p_add = Product.objects.create(
                original_price=original_price, vendor=vendor, name=name, brand=brand, size=size, tags=tags,
                category=category, subcategory=subcategory, product_for=product_for, discount=discount, stock=stock,
                price=price, delivery_charge=delivery_charge, desc=desc, pub_date=pub_date, image=myfile,
                image2=myfile2, image3=myfile3, )
            p_add.save()

            msg = "product added successfully"
            return render(request, "shop/add_product.html",
                          {'msg': msg, 'chartnum': chartnum, 'chartletter': chartletter,'form': form})
        else:
            form = AddproductForm()
            return render(request, "shop/add_product.html",
                          {'msg': msg, 'chartnum': chartnum, 'chartletter': chartletter,'form': form})
    else:
        return render(request, "shop/unauthorized.html", {'msg': msg,})


def viewmyproducts(request):
    if request.user.is_Vendor == True:
        vendor = getvendor(email=request.user.email)
        products = Product.objects.filter(vendor=vendor)
        params = {'products': products, 'vendor': vendor}
        print(params)
        print(vendor)
        return render(request, 'shop/myproduct.html', params)
    else:
        return render(request, "shop/unauthorized.html")


def updateproduct(request, myid):
    if request.user.is_Vendor == True:
        product = Product.objects.get(id=myid)
        product.size = convertstrtolist(product.size)
        if request.method == 'GET':
            name = request.GET.get('name')
            productid = request.GET.get('productid')
            # size = request.POST.getlist('size')
            # brand = request.POST['brand']
            # tags = request.POST.get('tags')
            category = request.GET.get('category')
            subcategory = request.GET.get('subcategory')
            product_for = request.GET.get('product_for')
            # discount = request.POST['discount']
            price = request.GET.get('selling_price')
            # stock = request.POST['stock']
            original_price = request.GET.get('price')
            # delivery_charge = request.POST['delivery_charge']
            desc = request.GET.get('desc', 'Description not available')
            print("hiii", product_for)
            Product.objects.filter(id=productid).update(name=name,
                                                        special_price=price, mrp=original_price, description=desc)

        return render(request, 'shop/update_product.html', {'product': product})
    else:
        return render(request, "shop/unauthorized.html")

# --------------------------------------------------------------
# general views
# --------------------------------------------------------------

# def listing(request):
#     # filter_by= request.GET.get('filter')
#     # condo_filter = ProductFilter(request.GET, queryset=condo_list)
#     product_list = Product.objects.all()
#     paginator = Paginator(product_list, 24) # Show 24 products per page.
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'shop/product-search.html', {'page_obj': page_obj})

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
PRODUCTS_PER_PAGE = 24

def listing(request):
    ordering = request.GET.get('ordering', "")  # http://www.wondershop.in:8000/listproducts/?page=1&ordering=price
    search = request.GET.get('search', "")
    price = request.GET.get('price', "")

    if search:
        product = Product.objects.filter(Q(name__icontains=search) | Q(
            brand__icontains=search)| Q(subcategory2__name__icontains=search)| Q(subcategory2__subcategory1__name__icontains=search)| Q(subcategory2__subcategory1__category__name__icontains=search))  # SQLite doesn’t support case-sensitive LIKE statements; contains acts like icontains for SQLite

    else:
        product = Product.objects.all()

    if ordering:
        product = product.order_by(ordering)

    if price:
        product = product.filter(special_price__lt=price)

    # Pagination
    page = request.GET.get('page', 1)
    product_paginator = Paginator(product, PRODUCTS_PER_PAGE)
    try:
        product = product_paginator.page(page)
    except EmptyPage:
        product = product_paginator.page(product_paginator.num_pages)
    except:
        product = product_paginator.page(PRODUCTS_PER_PAGE)
    return render(request, "shop/product-search.html",
                  {"product": product, 'page_obj': product, 'is_paginated': True, 'paginator': product_paginator})



