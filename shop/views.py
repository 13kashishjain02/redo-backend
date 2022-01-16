from django.shortcuts import render, redirect
from .models import Product, Order, Cart,Variation,Wishlist,SubCategory2,SubCategory1,Category
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
from django.db.utils import IntegrityError
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
    data = Order.objects.filter(user=request.user).values()
    print(data)
    # print(data[0].)

    return render(request, 'shop/myorder.html',{"orders":data})


def productView(request, slug):
    # Fetch the product using the id
    product = Product.objects.get(slug=slug)

    # if product.color:
    #     product.color = re.split('; | ,|, |,| |\n', product.color)
    if product.size:
        product.size = re.split('; | ,|, |,| |\n', product.size)

    if product.has_variation:
        variations = Variation.objects.filter(product=product)
        color=[]
        for i in variations:
            color.append(i.color)
        print(color)
        return render(request, 'shop/product_page_variation.html', {'product': product,'color':color})
    else:
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
        Cart.objects.filter(user=request.user).delete()
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
@login_required(login_url="../login")
def dashboard(request):
    return render(request, 'shop/dashboard.html')

@login_required(login_url="../login")
def addproduct(request):
    msg=""
    if request.user.is_Vendor:
        if request.method == 'POST':
            form = AddproductForm(request.POST, request.FILES)
            if form.is_valid():
                desc = form.cleaned_data['desc']
                short_desc = form.cleaned_data['short_desc']

            name = request.POST['product_name']
            vendor = getvendor(request.user.email)
            brand = request.POST['brand']
            tags = request.POST.get('tags')
            slug = name.replace(" ", "-")
            sprice = request.POST['sprice']
            mrp = request.POST['mrp']
            stock = request.POST['stock']
            weight = request.POST['weight']
            length = request.POST['length']
            width = request.POST['width']
            height = request.POST['height']
            material = request.POST['material']
            pub_date = date.today()
            myfile = request.FILES['myfile']
            myfile2 = request.FILES.get('myfile2')
            myfile3 = request.FILES.get('myfile3')
            types = request.POST.getlist('type')
            sku = request.POST['sku']
            category=request.POST['category']
            sub1 = request.POST.getlist('subcategory1')
            sub2 = request.POST['subcategory2']

            if types==None:
                is_ecofriendly=False
                is_upcycled = False
                is_recycled = False
            else:
                if '1' in types:
                    is_recycled=True
                else :
                    is_recycled = False
                is_upcycled=True if '2' in types else False
                is_ecofriendly=True if '3' in types else False

            for i in sub1:
                if i != 'Choose...':
                    subcategory1=i
                    break
                else:
                    subcategory1='Other'
            for i in sub2:
                if i != 'Choose...':
                    subcategory2=i
                else:
                    subcategory2='Other'

            try:
                category=Category.objects.get(name=category)
            except:
                category=Category.objects.create(name=category)
                category.save()
            try:
                subcategory1=SubCategory1.objects.get(name=subcategory1)
            except:
                subcategory1=SubCategory1.objects.create(name=subcategory1,category=category)
                subcategory1.save()
            try:
                subcategory2=SubCategory2.objects.get(name=subcategory2)
            except:
                subcategory2=SubCategory2.objects.create(name=subcategory2,subcategory1=subcategory1)
                subcategory2.save()


            try:
                p_add = Product.objects.create(
                    mrp=mrp, vendor=vendor, name=name, brand=brand,  tags=tags,
                    stock=stock,weight=weight,height=height,length=length,width=width,material=material,slug=slug,
                    special_price=sprice,  description=desc,short_description=short_desc, pub_date=pub_date, image=myfile,
                    image2=myfile2, image3=myfile3,in_stock=True ,is_recycled=is_recycled,is_upcycled=is_upcycled,is_ecofriendly=is_ecofriendly, subcategory1=subcategory1,category2=category,subcategory2=subcategory2,sku=sku)
                p_add.save()
            except IntegrityError as e:
                e = str(e)
                print(e)
                if e == "UNIQUE constraint failed: shop_product.slug":
                    msg = "Same SKU already exist"
                    return render(request, "shop/Add Product.html",
                                  {'msg': msg, 'form': form})
            msg = "product added successfully"
            return render(request, "shop/Add Product.html",
                          {'msg': msg,'form': form})
        else:
            form = AddproductForm()
            return render(request, "shop/Add Product.html",
                          {'msg': msg, 'form': form})
    else:
        return render(request, "shop/unauthorized.html", {'msg': msg,})

@login_required(login_url="../login")
def addvariation(request):
    msg=""
    if request.user.is_Vendor:
        if request.method == 'POST':
            form = AddproductForm(request.POST, request.FILES)
            if form.is_valid():
                desc = form.cleaned_data['desc']
                short_desc = form.cleaned_data['short_desc']

            name = request.POST['product_name']
            vendor = getvendor(request.user.email)
            brand = request.POST['brand']
            tags = request.POST.get('tags')
            slug = name.replace(" ", "-")
            sprice = request.POST['sprice']
            mrp = request.POST['mrp']
            stock = request.POST['stock']
            weight = request.POST['weight']
            length = request.POST['length']
            width = request.POST['width']
            height = request.POST['height']
            material = request.POST['material']
            pub_date = date.today()
            myfile = request.FILES['myfile']
            myfile2 = request.FILES.get('myfile2')
            myfile3 = request.FILES.get('myfile3')
            types = request.POST.getlist('type')
            sku = request.POST['sku']
            category=request.POST['category']
            sub1 = request.POST.getlist('subcategory1')
            sub2 = request.POST['subcategory2']

            if types==None:
                is_ecofriendly=False
                is_upcycled = False
                is_recycled = False
            else:
                if '1' in types:
                    is_recycled=True
                else :
                    is_recycled = False
                is_upcycled=True if '2' in types else False
                is_ecofriendly=True if '3' in types else False

            for i in sub1:
                if i != 'Choose...':
                    subcategory1=i
                    break
                else:
                    subcategory1='Other'
            for i in sub2:
                if i != 'Choose...':
                    subcategory2=i
                else:
                    subcategory2='Other'

            try:
                category=Category.objects.get(name=category)
            except:
                category=Category.objects.create(name=category)
                category.save()
            try:
                subcategory1=SubCategory1.objects.get(name=subcategory1)
            except:
                subcategory1=SubCategory1.objects.create(name=subcategory1,category=category)
                subcategory1.save()
            try:
                subcategory2=SubCategory2.objects.get(name=subcategory2)
            except:
                subcategory2=SubCategory2.objects.create(name=subcategory2,subcategory1=subcategory1)
                subcategory2.save()


            try:
                p_add = Product.objects.create(
                    mrp=mrp, vendor=vendor, name=name, brand=brand,  tags=tags,
                    stock=stock,weight=weight,height=height,length=length,width=width,material=material,slug=slug,
                    special_price=sprice,  description=desc,short_description=short_desc, pub_date=pub_date, image=myfile,
                    image2=myfile2, image3=myfile3,in_stock=True ,is_recycled=is_recycled,is_upcycled=is_upcycled,is_ecofriendly=is_ecofriendly, subcategory1=subcategory1,category2=category,subcategory2=subcategory2,sku=sku)
                p_add.save()
            except IntegrityError as e:
                e = str(e)
                print(e)

                if e == "UNIQUE constraint failed: shop_product.sku":
                    msg = "Same SKU already exist"
                    return render(request, "shop/add_variation.html",
                                  {'msg': msg, 'form': form})

                if e == "UNIQUE constraint failed: shop_product.slug":
                    msg = "Same Slug already exist, try changing product name"
                    return render(request, "shop/add_variation.html",
                                  {'msg': msg, 'form': form})


            vsprice1 = request.POST['vsprice1']
            if vsprice1:
                vmrp1 = request.POST['vmrp1']
                vstock1 = request.POST['vstock1']
                vsize1 = request.POST['vsizes1']
                vcolor1 = request.POST['color1']
                v1image1 = request.FILES['variation1_i1']
                v1image2 = request.FILES.get('variation1_i2')
                v1image3 = request.FILES.get('variation1_i3')
                v1_add = Variation.objects.create(
                    product=p_add,size=vsize1,color=vcolor1,stock=vstock1,mrp=vmrp1,special_price=vsprice1,image=v1image1,image2=v1image2,image3=v1image3
                )
                v1_add.save()

            vsprice2 = request.POST['vsprice2']
            if vsprice2:
                vmrp2 = request.POST['vmrp2']
                vstock2 = request.POST['vstock2']
                vsize2 = request.POST['vsizes2']
                vcolor2 = request.POST['color2']
                v2image1 = request.FILES['variation2_i1']
                v2image2 = request.FILES.get('variation2_i2')
                v2image3 = request.FILES.get('variation2_i3')
                v2_add = Variation.objects.create(
                    product=p_add, size=vsize2, color=vcolor2, stock=vstock1, mrp=vmrp2, special_price=vsprice2,
                    image=v2image1, image2=v2image2, image3=v2image3
                )
                v2_add.save()

            vsprice1 = request.POST['vsprice3']
            if vsprice1:
                vmrp1 = request.POST['vmrp3']
                vstock1 = request.POST['vstock3']
                vsize1 = request.POST['vsizes3']
                vcolor1 = request.POST['color3']
                v1image1 = request.FILES['variation3_i1']
                v1image2 = request.FILES.get('variation3_i2')
                v1image3 = request.FILES.get('variation3_i3')
                v1_add = Variation.objects.create(
                    product=p_add, size=vsize1, color=vcolor1, stock=vstock1, mrp=vmrp1, special_price=vsprice1,
                    image=v1image1, image2=v1image2, image3=v1image3
                )
                v1_add.save()

            vsprice1 = request.POST['vsprice4']
            if vsprice1:
                vmrp1 = request.POST['vmrp4']
                vstock1 = request.POST['vstock4']
                vsize1 = request.POST['vsizes4']
                vcolor1 = request.POST['color4']
                v1image1 = request.FILES['variation4_i1']
                v1image2 = request.FILES.get('variation4_i2')
                v1image3 = request.FILES.get('variation4_i3')
                v1_add = Variation.objects.create(
                    product=p_add, size=vsize1, color=vcolor1, stock=vstock1, mrp=vmrp1, special_price=vsprice1,
                    image=v1image1, image2=v1image2, image3=v1image3
                )
                v1_add.save()

            return render(request, "shop/add_variation.html",
                          {'msg': msg, 'form': form})
        else:
            form = AddproductForm()
            return render(request, "shop/add_variation.html",
                          {'msg': msg, 'form': form})
    else:
        return render(request, "shop/unauthorized.html", {'msg': msg,})

@login_required(login_url="../login")
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

@login_required(login_url="../login")
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

# def category(request):
#     # filter_by= request.GET.get('filter')
#     # condo_filter = ProductFilter(request.GET, queryset=condo_list)
#     product_list = Product.objects.filter()
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
    return render(request, "shop/search_result.html",
                  {"product": product, 'page_obj': product, 'is_paginated': True, 'paginator': product_paginator})
    # return render(request, "shop/category.html",
    #               {"product": product, 'page_obj': product, 'is_paginated': True, 'paginator': product_paginator})


def wishlist(request):
    try:
        list = Wishlist.objects.get(user=request.user)
        data=list.wishlist

        print("hello!",data)
        counter=0
        total=0
        final_total=0
        print("trt")
        return render(request, 'shop/wishlist.html')
    except Exception as e:
        print("except",e)
        return render(request, 'shop/wishlist.html')

import datetime

def vendororders(request):
    data = Order.objects.all()
    data=data.values()



    return render(request, 'shop/vendororders.html')