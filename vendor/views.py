from itertools import count, product
from sre_parse import State
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
import re
from account.views import password_pattern,phone_pattern,User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from account.models import VendorAccount
from shop.models import Product,Variation
from shop.forms import StateForm
from django.views.decorators.csrf import csrf_exempt

def register(request):
    context = {}
    if request.method == 'POST':
        email = 'email' in request.POST and request.POST['email']
        password = 'password' in request.POST and request.POST['password']
        contact = 'contact' in request.POST and request.POST['contact']

        context['email_v'] = email
        context['password_v'] = password
        context['contact_v'] = contact

        if User.objects.filter(email=email).exists():
            if User.objects.get(email=email).is_Vendor:
                context['email'] = 'This email address is already exists'

        elif not re.search(password_pattern,password):
            context['password'] = 'Your password must contain at 8 charcters, at least 1 number, 1 uppercase and 1 non-alphanumeric character.'
        
        elif User.objects.filter(contact_number=contact).exists():
            context['contact'] = 'This phone number is already exists'

        elif not re.search(phone_pattern,contact):
            context['contact1'] = 'Phone number is not valid'
            
        else:
            User.objects.create(
                email = email,
                password = make_password(password),
                contact_number = contact,
                is_Vendor = True
            )
            context['email_v'] = ''
            context['password_v'] = ''
            context['contact_v'] = ''
            messages.success(request,'Account Created')


    return render(request,'vendor/register.html',context=context)


def vendorLogin(request):
    context = {}
    if request.method == "POST":
        email = 'email' in request.POST and request.POST['email']
        password = 'password' in request.POST and request.POST['password']
        
        context['email'] = email
        context['password'] = password
        
        user = authenticate(email=email,password=password)

        if user is not None:
            if User.objects.get(email=email).is_Vendor:
                login(request,user)
                return redirect('/vendor/account/')
        else:
            messages.error(request,'Email or password is invalid')


    return render(request, 'vendor/login.html',context=context)



def accountVendor(request):
    if request.user.is_authenticated and request.user.is_Vendor:
        if request.method == "POST":
            email = 'email' in request.POST and request.POST['email']
            shop_name = 'shop_name' in request.POST and request.POST['shop_name']
            shop_number = 'shop_number' in request.POST and request.POST['shop_number']
            state = 'state' in request.POST and request.POST['state']
            city = 'city' in request.POST and request.POST['city']
            pincode = 'pincode' in request.POST and request.POST['pincode']
            shop_address = 'shop_address' in request.POST and request.POST['shop_address']
            gst_number = 'gst_number' in request.POST and request.POST['gst_number']
            vat_number = 'vat_number' in request.POST and request.POST['vat_number']
            pan_number = 'pan_number' in request.POST and request.POST['pan_number']
            company_pan_number = 'company_pan_number' in request.POST and request.POST['company_pan_number']
            bank_name = 'bank_name' in request.POST and request.POST['bank_name']
            bank_account_holder_name = 'bank_account_holder_name' in request.POST and request.POST['bank_account_holder_name']
            bank_account_number = 'bank_account_number' in request.POST and request.POST['bank_account_number']
            bank_ifsc_code = 'bank_ifsc_code' in request.POST and request.POST['bank_ifsc_code']

            v = VendorAccount.objects.get(email = request.user)
            v.email = email
            v.shop_name = shop_name
            v.shop_number = shop_number 
            v.state = state
            v.city = city
            v.pincode = pincode
            v.shop_add = shop_address
            v.gst = gst_number
            v.vat = vat_number
            v.pan = pan_number
            v.companypan = company_pan_number
            v.bank_name = bank_name
            v.bank_account_holder_name = bank_account_holder_name
            v.bank_account_number = bank_account_number
            v.bank_ifsc_code = bank_ifsc_code
            v.save()
            
            messages.success(request,'Account Updated Successfully')

        return render(request,'vendor/account.html')
    return redirect('/vendor/login/') 


def documents(request):
    if request.user.is_authenticated and request.user.is_Vendor:
        if request.method == "POST":
            pan = 'pan' in request.FILES and request.FILES['pan']
            addhaar = 'aadhaar' in request.FILES and request.FILES['aadhaar']
            c_pan = 'c-pan' in request.FILES and request.FILES['c-pan']

            v = VendorAccount.objects.get(email=request.user)
            v.pan_image = pan
            v.aadhaar_image = addhaar
            v.companypan_image = c_pan
            v.save()
    
        return render(request,'vendor/documents.html')
    return redirect('/vendor/login/')

def addProducts(request):
    category_validation = ""
    sub_category_1_validation = ""
    sub_category_2_validation = ""
    sub_category_3_validation = ""
    p_name = ""
    b_name = ""
    sku = ""
    weight = ""
    length = ""
    width = ""
    height = ""
    mrp = ""
    s_price = ""
    stock = ""
    rec = ""
    upc = ""
    eco = ""
    handi = ""
    handl = ""
    p_tags = ""
    material = ""
    category = ""
    sub_category1 = ""
    s_desc = ""
    l_desc = ""
    sub_category2 = ""

    if request.user.is_authenticated and request.user.is_Vendor and  request.user.vendoraccount.is_verified:
        if request.method == "POST":
            state = StateForm(request.POST)
            if state.is_valid():
                st = state.cleaned_data['state']

            p_name = 'p_name' in request.POST and request.POST['p_name']
            b_name = 'b_name' in request.POST and request.POST['b_name']
            sku = 'sku' in request.POST and request.POST['sku']
            weight = 'weight' in request.POST and request.POST['weight']
            length = 'length' in request.POST and request.POST['length']
            width = 'width' in request.POST and request.POST['width']
            height = 'height' in request.POST and request.POST['height']
            mrp = 'mrp' in request.POST and request.POST['mrp']
            s_price = 's_price' in request.POST and request.POST['s_price']
            stock = 'stock' in request.POST and request.POST['stock']
            recycled = 'recycled' in request.POST and request.POST['recycled']
            upcycled = 'upcycled' in request.POST and request.POST['upcycled']
            ecofriendly = 'ecofriendly' in request.POST and request.POST['ecofriendly']
            handicraft = 'handicraft' in request.POST and request.POST['handicraft']
            handloom = 'handloom' in request.POST and request.POST['handloom']
            p_image1 = 'p_image1' in request.FILES and request.FILES['p_image1']
            p_image2 = 'p_image2' in request.FILES and request.FILES['p_image2']
            p_image3 = 'p_image3' in request.FILES and request.FILES['p_image3']
            p_image4 = 'p_image4' in request.FILES and request.FILES['p_image4']
            p_tags = 'p_tags' in request.POST and request.POST['p_tags']
            material = 'material' in request.POST and request.POST['material']
            category = 'category' in request.POST and request.POST['category']
            sub_category1 = 'sub_category1' in request.POST and request.POST['sub_category1']
            sub_category2 = 'sub_category2' in request.POST and request.POST['sub_category2']
            sub_category3 = 'sub_category3' in request.POST and request.POST['sub_category3']
            s_desc = 's_desc' in request.POST and request.POST['s_desc']
            l_desc = 'l_desc' in request.POST and request.POST['l_desc']
            sizes = 'sizes' in request.POST and request.POST['sizes']
            gst = 'gst' in request.POST and request.POST['gst']

            
            
            rec = False
            if recycled:
                rec = True
            
            upc = False
            if upcycled:
                upc = True

            eco= False
            if ecofriendly:
                eco = True
            
            handi = False
            if handicraft:
                handi = True

            handl= False
            if handloom:
                handl = True
              
            
            v_account = VendorAccount.objects.get(vendor=request.user)

           
            if category == "Choose":
                category_validation = "Please Choose the category"
            elif sub_category1 == "Choose":
                sub_category_1_validation = "Please Choose the subcateogry"
            elif sub_category2 == "Choose":
                sub_category_2_validation = "Please Choose the subcateogry"
            elif sub_category3 == "Choose":
                sub_category_3_validation = "Please Choose the subcateogry"

            else:
                try:
                    Product.objects.create(
                    vendor = v_account,
                    name = p_name,
                    brand = b_name,
                    sku = sku,
                    weight = weight,
                    length = length,
                    width = width,
                    height = height,
                    mrp = mrp,
                    special_price = s_price,
                    stock =stock,
                    image = p_image1,
                    image2 = p_image2,
                    image3 = p_image3,
                    image4 = p_image4,
                    tags = p_tags,
                    material = material,
                    category = category,
                    subcategory1 = sub_category1,
                    subcategory2 = sub_category2,
                    subcategory3 = sub_category3,
                    description = l_desc,
                    short_description = s_desc,
                    is_recycled = rec,
                    is_upcycled = upc,
                    is_ecofriendly= eco,
                    state = st,
                    size = sizes,
                    is_handicraft = handi,
                    is_handloom=handl,
                    gst = gst
                    
                )
                except:
                    pass
                category_validation = ""
                sub_category_1_validation = ""
                sub_category_2_validation = ""
                sub_category_3_validation = ""
                p_name = ""
                b_name = ""
                sku = ""
                weight = ""
                length = ""
                width = ""
                height = ""
                mrp = ""
                s_price = ""
                stock = ""
                rec = ""
                upc = ""
                eco = ""
                p_tags = ""
                material = ""
                category = ""
                sub_category1 = ""
                s_desc = ""
                l_desc = ""
                sub_category2 = ""

        
        state = StateForm()  
        context = {'p_name':p_name,'b_name':b_name,"sku":sku,
                    "weight":weight,"length":length,"width":width,
                    "height":height,'mrp':mrp,"s_price":s_price,"stock":stock,
                    "p_tags":p_tags,"material":material,"category":category,"sub_category1":sub_category1,"l_desc":l_desc,
                    "s_desc":s_desc,"rec":rec,"upc":upc,"eco":eco,"handl":handl,"handi":handi,"state":state,"c_validation":category_validation,"s1_validation":sub_category_1_validation, "s2_validation":sub_category_2_validation,"s3_validation":sub_category_3_validation}     
        return render(request,'vendor/add-products.html',context=context)
    return redirect('/vendor/documents/upload/')



def addProductVariation(request):
    if request.user.is_authenticated and request.user.is_Vendor and  request.user.vendoraccount.is_verified:
        state = StateForm()  
        context = {"state":state}     
        return render(request,'vendor/add-products-variation.html',context=context)
    return redirect('/vendor/documents/upload/')

@csrf_exempt
def storeVproducts(request):
    # request.session['length'] = 1
    if request.method == "POST" and 'add_more' in request.POST:
        request.session['length'] = request.POST['length']
    
    elif request.method == "POST" and 'save' in request.POST:
        p_name = 'p_name' in request.POST and request.POST['p_name']
        b_name = 'b_name' in request.POST and request.POST['b_name']
        weight = 'weight' in request.POST and request.POST['weight']
        length = 'length' in request.POST and request.POST['length']
        width = 'width' in request.POST and request.POST['width']
        height = 'height' in request.POST and request.POST['height']
        recycled = 'recycled' in request.POST and request.POST['recycled']
        upcycled = 'upcycled' in request.POST and request.POST['upcycled']
        ecofriendly = 'ecofriendly' in request.POST and request.POST['ecofriendly']
        handicraft = 'handicraft' in request.POST and request.POST['handicraft']
        handloom = 'handloom' in request.POST and request.POST['handloom']
        p_tags = 'p_tags' in request.POST and request.POST['p_tags']
        material = 'material' in request.POST and request.POST['material']
        category = 'category' in request.POST and request.POST['category']
        sub_category1 = 'sub_category1' in request.POST and request.POST['sub_category1']
        sub_category2 = 'sub_category2' in request.POST and request.POST['sub_category2']
        sub_category3 = 'sub_category3' in request.POST and request.POST['sub_category3']
        s_desc = 's_desc' in request.POST and request.POST['s_desc']
        l_desc = 'l_desc' in request.POST and request.POST['l_desc']
        sizes = 'sizes' in request.POST and request.POST['sizes']
        gst = 'gst' in request.POST and request.POST['gst']
        
        v_account = VendorAccount.objects.get(vendor=request.user)

        rec = False
        if recycled:
            rec = True
        
        upc = False
        if upcycled:
            upc = True

        eco= False
        if ecofriendly:
            eco = True
        
        handi = False
        if handicraft:
            handi = True

        handl= False
        if handloom:
            handl = True

        state = StateForm(request.POST)
        if state.is_valid():
            st = state.cleaned_data['state']

        p = Product(
                    vendor = v_account,
                    name = p_name,
                    brand = b_name,
                    weight = weight,
                    length = length,
                    width = width,
                    height = height,
                    tags = p_tags,
                    material = material,
                    category = category,
                    subcategory1 = sub_category1,
                    subcategory2 = sub_category2,
                    subcategory3 = sub_category3,
                    description = l_desc,
                    short_description = s_desc,
                    is_recycled = rec,
                    is_upcycled = upc,
                    is_ecofriendly= eco,
                    state = st,
                    size = sizes,
                    is_handicraft = handi,
                    is_handloom=handl,
                    gst = gst,
                    has_variation = True
        )
        p.save()
        p_id = Product.objects.get(id=p.id)
        
        try :
            if 'length' in request.session:
                for i in range(int(request.session['length'])):
                    Variation.objects.create(product=p_id,
                    size= f'size{i+1}' in request.POST and request.POST[f'size{i+1}'],
                    sku= f'sku{i+1}' in request.POST and request.POST[f'sku{i+1}'],
                    color= f'color{i+1}' in request.POST and request.POST[f'color{i+1}'],
                    image1= f'p_image1{i+1}' in request.FILES and request.FILES[f'p_image1{i+1}'],
                    image2= f'p_image2{i+1}' in request.FILES and request.FILES[f'p_image2{i+1}'],
                    image3= f'p_image3{i+1}' in request.FILES and request.FILES[f'p_image3{i+1}'],
                    mrp= f'mrp{i+1}' in request.POST and request.POST[f'mrp{i+1}'],
                    stock= f'stock{i+1}'in request.POST and request.POST[f'stock{i+1}'],
                    special_price= f'price{i+1}' in request.POST and request.POST[f'price{i+1}'])
                del request.session['length']
                messages.success(request,'Product has been added')
        
            else:
                Variation.objects.create(product=p_id,
                    size= 'size1' in request.POST and request.POST['size1'],
                    sku= 'sku1' in request.POST and request.POST['sku1'],
                    color= 'color1' in request.POST and request.POST['color1'],
                    image1= 'p_image11' in request.FILES and request.FILES['p_image11'],
                    image2= 'p_image21' in request.FILES and request.FILES['p_image21'],
                    image3= 'p_image31' in request.FILES and request.FILES['p_image31'],
                    mrp= 'mrp1' in request.POST and request.POST['mrp1'],
                    stock= 'stock1' in request.POST and request.POST['stock1'],
                    special_price= 'price1' in request.POST and request.POST['price1'])

                messages.success(request,'Product has been added')
        except:
            messages.success(request,'Product has been added')
            
        


    return redirect('/vendor/add-products/variations/')

def products(request):
    vendor = VendorAccount.objects.get(vendor=request.user)
    products = Product.objects.filter(vendor=vendor)
    return render(request,'vendor/products.html',{'products':products})

def edit_products(request,id):
    v_product = Product.objects.get(id=id)
    if request.user.is_authenticated and request.user.is_Vendor and  request.user.vendoraccount.is_verified:
        if request.method == "POST":
            state = StateForm(request.POST)
            if state.is_valid():
                st = state.cleaned_data['state']

            p_name = 'p_name' in request.POST and request.POST['p_name']
            b_name = 'b_name' in request.POST and request.POST['b_name']
            sku = 'sku' in request.POST and request.POST['sku']
            weight = 'weight' in request.POST and request.POST['weight']
            length = 'length' in request.POST and request.POST['length']
            width = 'width' in request.POST and request.POST['width']
            height = 'height' in request.POST and request.POST['height']
            mrp = 'mrp' in request.POST and request.POST['mrp']
            s_price = 's_price' in request.POST and request.POST['s_price']
            stock = 'stock' in request.POST and request.POST['stock']
            recycled = 'recycled' in request.POST and request.POST['recycled']
            upcycled = 'upcycled' in request.POST and request.POST['upcycled']
            ecofriendly = 'ecofriendly' in request.POST and request.POST['ecofriendly']
            handicraft = 'handicraft' in request.POST and request.POST['handicraft']
            handloom = 'handloom' in request.POST and request.POST['handloom']
            p_image1 = 'p_image1' in request.FILES and request.FILES['p_image1']
            p_image2 = 'p_image2' in request.FILES and request.FILES['p_image2']
            p_image3 = 'p_image3' in request.FILES and request.FILES['p_image3']
            p_image4 = 'p_image4' in request.FILES and request.FILES['p_image4']
            p_tags = 'p_tags' in request.POST and request.POST['p_tags']
            material = 'material' in request.POST and request.POST['material']
            category = 'category' in request.POST and request.POST['category']
            sub_category1 = 'sub_category1' in request.POST and request.POST['sub_category1']
            sub_category2 = 'sub_category2' in request.POST and request.POST['sub_category2']
            sub_category3 = 'sub_category3' in request.POST and request.POST['sub_category3']
            s_desc = 's_desc' in request.POST and request.POST['s_desc']
            l_desc = 'l_desc' in request.POST and request.POST['l_desc']
            sizes = 'sizes' in request.POST and request.POST['sizes']
            gst = 'gst' in request.POST and request.POST['gst']

            
            
            rec = False
            if recycled:
                rec = True
            
            upc = False
            if upcycled:
                upc = True

            eco= False
            if ecofriendly:
                eco = True
            
            handi = False
            if handicraft:
                handi = True

            handl= False
            if handloom:
                handl = True
              
            
            v_product.name = p_name
            v_product.brand = b_name
            v_product.tags = p_tags
            v_product.material = material
            v_product.sku = sku
            v_product.stock = stock
            v_product.mrp = mrp
            v_product.special_price = s_price
            v_product.description = l_desc
            v_product.short_description = s_desc
            v_product.weigth = weight
            v_product.length = length
            v_product.weigth = weight
            v_product.heigth = height
            v_product.state = st
            v_product.gst = gst

            if recycled:
                v_product.is_recycled = True
            if upcycled:
                v_product.is_upcycled = True
            if recycled:
                v_product.is_recycled = True
            if ecofriendly:
                v_product.is_ecofriendly = True
            if handicraft:
                v_product.is_handicraft = True
            if handloom:
                v_product.is_handloom = True

            if p_image1:
                v_product.image = p_image1
            if p_image2:
                v_product.image2 = p_image2
            if p_image3:
                v_product.image3 = p_image3
            if p_image4:
                v_product.image4 = p_image4

            if category and category != 'Choose':
                v_product.category = category
            if sub_category1 and sub_category1 != 'Choose':
                v_product.subcategory1 = sub_category1
            if sub_category2 and sub_category2 != 'Choose':
                v_product.subcategory2 = sub_category2
            if sub_category3 and sub_category3 != 'Choose':
                v_product.subcategory3 = sub_category3
            
            
            

            v_product.save()
            messages.success(request,'Product has been updated')

        state = StateForm(instance=v_product)
        product = Product.objects.get(id=id)
        return render(request,'vendor/edit-product.html',{'product':product,'state':state})
    return redirect('/vendor/add-products/variations/')

def orders(request):
    return render(request,'vendor/orders.html')
    