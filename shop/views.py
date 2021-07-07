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

MERCHANT_KEY = 'Ujzdeai9L@l%#6!o';
username = ""
orderid = ""
# msg is for time when the message has to be printed on same page
msg = ""
# msessage is for time when the message has to be printed on some other page such as index
message = ""


# ----------------------------------------------------------
# static methods
# ----------------------------------------------------------

def getvendor(email):
    vendor = VendorAccount.objects.get(email=email)
    return vendor


def getvendorbyshopname(shop_name):
    vendor = VendorAccount.objects.get(shop_name=shop_name)
    return vendor


def sorting(array, stype):
    if stype == "pricehigh":
        # To sort the list in place...
        array.sort(key=lambda x: x.price, reverse=True)
        # To return a new list, use the sorted() built-in function...
        array = sorted(array, key=lambda x: x.price, reverse=True)

    if stype == "pricelow":
        # To sort the list in place...
        array.sort(key=lambda x: x.price, reverse=False)
        # To return a new list, use the sorted() built-in function...
        array = sorted(array, key=lambda x: x.price, reverse=False)

    if stype == "latest":
        # To sort the list in place...
        array.sort(key=lambda x: x.pub_date, reverse=True)
        # To return a new list, use the sorted() built-in function...
        array = sorted(array, key=lambda x: x.pub_date, reverse=True)

    return array


def filtering(array, prodfor, category):
    if prodfor is not None:
        array = array.filter(product_for=prodfor)
    if category is not None:
        array = array.filter(category=category)
    return array


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


def searchMatch(query, item):
    '''return true only if query matches the item'''
    print("hello", item.subcategory, item.tags)
    if query in item.desc.lower() or query in item.name.lower() or query in item.tags.lower() or query in item.category.lower() or query in item.subcategory.lower() or query in item.product_for.lower() or query in item.vendor.shop_name.lower():
        return True
    else:
        return False


# --------------------------------------------------------------
# general views
# --------------------------------------------------------------


def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    for i in product:
        i.size = convertstrtolist(i.size)

    return render(request, 'shop/detail.html', {'product': product[0]})


@login_required(login_url="../login")
def placeorder(request):
    if request.method == 'POST':
        username = request.user.email
        receivers_add = request.POST['receivers_add']
        city = request.POST['city']
        state = request.POST['state']
        receivers_pincode = request.POST['receivers_pincode']
        receivers_landmark = request.POST['receivers_landmark']
        receivers_contact = request.POST['receivers_contact']
        payment = request.POST['payment']
        a, total = olist(username)
        order_list = ""

        receivers_add = receivers_add + ", " + city + ", " + state

        for i in a:
            order_list = order_list + "[ product id : " + str(i["product_id"]) + ", vendor : " + i[
                "vendor"] + ", price : " + str(i["price"]) + ", qty : " + str(i["qty"]) + "]"

        c_order = Order.objects.create(username=username, order_list=order_list, receivers_pincode=receivers_pincode,
                                       receivers_add=receivers_add, receivers_contact=receivers_contact,
                                       receivers_landmark=receivers_landmark, total=total)
        c_order.save()
        global orderid
        orderid = str(c_order.id)
        # return redirect('../paytmcheckout')
        url = '../payucheckout/' + str(total)
        return redirect(url)
    else:
        return render(request, 'shop/placeorder.html')


def search(request):
    query = request.GET.get('search').lower()
    prodfor = request.GET.get('prodfor')
    sort = request.GET.get('sort')
    category = request.GET.get('category')
    allProds = []
    prodtemp = Product.objects.all()
    if prodfor or category is not None:
        prodtemp = filtering(prodtemp, prodfor, category)

    analyzed = ""
    for char in query:
        if char != " ":
            analyzed = analyzed + char
            if len(analyzed) == len(query):
                prod = [item for item in prodtemp if searchMatch(analyzed, item)]
                if len(prod) != 0:
                    allProds.append(prod)


        else:
            prod = [item for item in prodtemp if searchMatch(analyzed, item)]
            if len(prod) != 0:
                allProds.append(prod)

            analyzed = ""

    temp = []
    for product in allProds:
        for i in product:
            temp.append(i)
    if sort is not None:
        temp = sorting(temp, sort)

    allProds = temp
    params = {'allProds': allProds, "msg": "", "query": query}

    if len(allProds) == 0:
        params = {'msg': "No result found, we are adding new products daily so make sure to check again later",
                  "query": query}

    return render(request, 'shop/search_result.html', params)
    # return render(request, 'costumer/product.html', params)

def listing(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 24) # Show 24 products per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/list.html', {'page_obj': page_obj})

# ---------------------------------------------------------------------
# vendor related functions
# ---------------------------------------------------------------------

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
        return render(request, 'shop/vendorproducts.html', params)
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
            Product.objects.filter(id=productid).update(name=name, category=category, subcategory=subcategory,
                                                        price=price, original_price=original_price, desc=desc)

        return render(request, 'shop/updateproduct.html', {'product': product})
    else:
        return render(request, "shop/unauthorized.html")
