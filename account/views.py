from email import message
import email
from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from .models import Account, VendorAccount, BloggerAccount
# from cart.models import Cartdata
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, login, authenticate
import requests
import json
from datetime import date
from django.core.files.storage import default_storage
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum2
from django.http import HttpResponseRedirect, HttpResponse
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import re
from .helpers import mail
import uuid
from .models import Unique,Profile,Address

User = get_user_model()
phone_pattern = '^\+?1?\d{9,15}$'
password_pattern = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

# ---------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------
MERCHANT_KEY = 'Ujzdeai9L@l%#6!o'
otp=""
msg = ""


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def otpemail(request,remail='kashish.iitdelhi@gmail.com',sub="Redopact",msg="Thank you for registering to our site"):
    global otp
    print("global otp",otp)
    print(remail,"email")
    if request.method == 'POST':
        print("here")
        otp_check = request.POST.get('otp')
        print(otp,otp_check)
        if otp == otp_check:
            user=Account.objects.get(email=remail)
            vendor=VendorAccount.objects.get(email=remail)
            vendor.is_verified = True
            vendor.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('../../dashboard')
        else:
            print("wrong otp")
            return render(request, "account/otp.html",{msg:'wrong otp'})
    else:

        otp =str(random.randint(1000, 9999))
        print("otp is :",otp)
        subject = sub
        message = otp
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [remail, ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, "account/otp.html")

# -----------------------------------------------------------------------

# User Regsitration


def userregister(request):
    context = {}
    if request.method == 'POST':
        email = 'email' in request.POST and request.POST['email']
        password = 'password' in request.POST and request.POST['password']
        contact = 'contact' in request.POST and request.POST['contact']

        context['email_v'] = email
        context['password_v'] = password
        context['contact_v'] = contact

        if User.objects.filter(email=email).exists():
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
                contact_number = contact
            )
            context['email_v'] = ''
            context['password_v'] = ''
            context['contact_v'] = ''
            messages.success(request,'Account Created')

        

        
    return render(request, "account/register.html",context=context)


# ----------------------------------------------------------------
# User Login

def userlogin(request):
    context = {}
    if request.method == "POST":
        email = 'email' in request.POST and request.POST['email']
        password = 'password' in request.POST and request.POST['password']
        
        context['email'] = email
        context['password'] = password
        
        user = authenticate(email=email,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'Welcome to Redopact. You are authenticated')
            return redirect('/')
        else:
            messages.error(request,'Email or password is invalid')


    return render(request, 'account/login.html',context=context)


# ----------------------------------------------------------------
# Reset password


def reset(request):
    context = {}
    if request.method == "POST":
        email = 'email' in request.POST and request.POST['email']
        context['email_v'] = email
        if User.objects.filter(email=email).exists():
            generate_new_uuid = uuid.uuid4()
            user = User.objects.get(email=email)
            change_uuid = Unique.objects.get(user=user)
            change_uuid.uuid = generate_new_uuid
            change_uuid.save()

            get_uuid = Unique.objects.get(user=user)
            mail(
                message=f'Reset password link - http://127.0.0.1:8000/reset-password/{get_uuid.uuid}',
                subject='Reset Password',
                email=email
            )

            messages.success(request,'A reset password link has been send to your email')
        else:
            context['email'] = "Sorry !! we didn't find any account with this email address "
           
    return render(request,'account/reset.html',context=context)



def reset_password(request,uid):
    context = {}
    try:
        if Unique.objects.filter(uuid=uid).exists():
            if request.method == "POST":
                password = 'password' in request.POST and request.POST['password']

                if not re.search(password_pattern,password):
                    context['password'] = 'Your password must contain at 8 charcters, at least 1 number, 1 uppercase and 1 non-alphanumeric character.'
                
                else:
                    get_user_email = Unique.objects.get(uuid=uid)
                    change_password = User.objects.get(email=get_user_email.user)
                    change_password.password = make_password(password)
                    change_password.save()

                    #change uuid
                    chng_uuid = Unique.objects.get(user=get_user_email.user)
                    chng_uuid.uuid = uuid.uuid4()
                    chng_uuid.save()

                    messages.success(request,'Your password has been changed successfully !!')
                    return redirect('/login/')
        else:
            return redirect('/login/')

    except:
        return redirect('/login/')
    
    return render(request,'account/reset_password.html',context=context)




# ----------------------------------------------------------------
# Edit profile



@login_required
def edit_profile(request):
    if request.method == "POST":
        email = 'email' in request.POST and request.POST['email']
        contact = 'contact' in request.POST and request.POST['contact']
        name = 'name' in request.POST and request.POST['name']
        location = 'location' in request.POST and request.POST['location']
        image = 'image' in request.FILES and request.FILES['image']
        gender = 'gender' in request.POST and request.POST['gender']
        dob = 'dob' in request.POST and request.POST['dob']

        user = User.objects.get(email=request.user)
        user.email = email
        user.contact_number = contact
        user.name = name
        print(image)
        profile = Profile.objects.get(user=request.user)
        if image:
            profile.image = image
        profile.gender = gender
        profile.dob = dob
        profile.location = location

        profile.save()
        user.save()
    
        messages.success(request,'Profile has been updated !!')
    return render(request,'account/edit-profile.html')




# ----------------------------------------------------------------
# address


@login_required
def address(request):
    if request.method == "POST" and 'edit-address' in request.POST:
        id = 'id' in request.POST and request.POST['id']
        pincode = 'pincode' in request.POST and request.POST['pincode']
        state = 'state' in request.POST and request.POST['state']
        address = 'address' in request.POST and request.POST['address']
        town = 'town' in request.POST and request.POST['town']
        city = 'city' in request.POST and request.POST['city']

        update_address = Address.objects.get(id=id)
        update_address.pincode = pincode
        update_address.state = state
        update_address.address = address
        update_address.town = town
        update_address.city = city

        update_address.save()

        messages.success(request,'Address has been updated !!')
    
    elif request.method == "POST" and 'remove-address' in request.POST:
        id = 'id' in request.POST and request.POST['id']
        count = Address.objects.filter(user=request.user).count()
        if count <= 1:
            messages.error(request,'You cannot remove this address ')
        else:
            Address.objects.get(id=id).delete()
            messages.success(request,'Address has been removed !!')

    elif request.method == "POST" and 'add-address' in request.POST:
        pincode = 'pincode' in request.POST and request.POST['pincode']
        state = 'state' in request.POST and request.POST['state']
        address = 'address' in request.POST and request.POST['address']
        town = 'town' in request.POST and request.POST['town']
        city = 'city' in request.POST and request.POST['city']

        Address.objects.create(
            user = request.user,
            pincode = pincode,
            state = state,
            address = address,
            town = town,
            city = city
        )

        messages.success(request,'New address has been added !!')
            



    addressess = Address.objects.filter(user=request.user)

    return render(request,'account/address.html',context={'addressess':addressess})




# ----------------------------------------------------------------
# orders

@login_required
def orders(request):
    return render(request,'account/orders.html')

@login_required
def order_details(request):
    print(request.GET.get('Order_Id'))
    return render(request,'account/order-details.html')





@login_required(login_url="../login")
def logoutuser(request):
    logout(request)
    return redirect("../")


















# @login_required(login_url="../login")
def vendorregister(request):


    if request.method == 'POST':
        name = request.POST['name']
        shop_number = request.POST.get('shop_number')
        email = request.POST['email']
        password = request.POST.get('password')
        try:
            user = Account.objects.create_user(
                name=name, email=email, password=password, contact_number=shop_number, viewpass=password
            )
            user.save()
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            msg = "User Registration Successful"
        except IntegrityError as e:
            msg = email + " is already registered,if you think there is a issue please contact us at 6264843506"
            olduser = authenticate(email=email, password=password)
            if olduser:
                pass
            else:
                msg="this email is already registered as a user, please enter the correct password to become a vendor"
                return render(request, "account/vendor_signup.html", {'msg': msg})
        except Exception as e:
            print(e)
            msg=e


        shopname = request.POST.get('shopname').lower()
        gst = request.POST.get('gst')
        shop_add_flat = request.POST['address']
        shop_add_city = request.POST['city']
        shop_add_state = request.POST['state']

        user=Account.objects.get(email=email)
        user.is_Vendor = True
        user.save()
        try:
            user = VendorAccount.objects.create(
                shop_name=shopname, shop_number=shop_number, shop_add=shop_add_flat, city=shop_add_city,
                state=shop_add_state, gst=gst, vendor=user, email=email)
            user.save()

        except IntegrityError as e:
            e = str(e)
            if e == "UNIQUE constraint failed: account_vendoraccount.shop_name":
                shopname = shopname + "#" + name[2:5]

                user = VendorAccount.objects.create(
                    shop_name=shopname, shop_number=shop_number, shop_add=shop_add, gst=gst, vendor=user, email=email)
                user.save()
            else:
                vendor=VendorAccount.objects.get(email=email)
                if vendor.is_verified:
                    msg = "vendor already registered,if you think there is a issue please contact us "
                    return render(request, "account/vendor_signup.html", {'msg': msg})


        msg = "Vendor Registration Successful"
        return redirect('../otpemail/'+email)
        # otpemail(request,remail=email)
    else:
        return render(request, "account/vendor_signup.html")


@login_required(login_url="../login")
def bloggerregister(request):
    if request.method == 'POST':
        email = request.user.email
        blogname = request.POST['blogname'].lower()
        bio = request.POST.get('bio')
        shop_add_flat = request.POST['shop_add_flat']
        shop_add_city = request.POST['shop_add_city']
        shop_add_state = request.POST['shop_add_state']
        shop_add_pincode = str(request.POST.get('shop_add_pincode'))
        # shop_add = shop_add_flat + "," + shop_add_city + "," + shop_add_state + "," + shop_add_pincode
        plan = request.POST.get('plan')
        subscription_amount = 50
        blogger = Account.objects.get(email=email)
        blogger.is_Blogger = True
        blogger.save()
        promocode = request.POST.get('promocode')
        print("here")
        try:
            print("here")
            user = BloggerAccount.objects.create(
                blogname=blogname, address=shop_add_flat, city=shop_add_city,
                state=shop_add_state, plan=plan, blogger=blogger,
                subscripton_amount=subscription_amount, email=email)
            user.save()
            print("here save successfull")

        except IntegrityError as e:
            e = str(e)
            print("here")
            print(e)
            if e == "UNIQUE constraint failed: account_bloggeraccount.blogname":
                blogname = blogname + "#" + blogger.name[2:5]

                user = BloggerAccount.objects.create(
                    blogname=blogname, address=shop_add_flat, city=shop_add_city,
                    state=shop_add_state, plan=plan, blogger=blogger,
                    subscripton_amount=subscription_amount, email=email)
                user.save()
            else:
                msg = "vendor already registered,if you think there is a issue please contact us at 6264843506"
                return render(request, "account/blogger_registeration.html", {'msg': msg})

        # twilio message
        # account_sid = 'AC58aae686ada0a42728e123cfee24cd5b'
        # auth_token = '1d2bfa8c3b98e92dd3d9c271fba9463e'
        # client = Client(account_sid, auth_token)
        #
        # message = client.messages \
        #     .create(
        #     body="a new vendor has registored, email=" + email + "shopname =" + shopname + "and contact_number is " + str(
        #         mobile),
        #     from_='+14159696324',
        #     to='+916264843506'
        # )

        # print(message.sid)

        # return redirect("../subscription")
        return redirect("../")
    else:
        return render(request, "account/blogger_registeration.html")


@login_required(login_url="../login")
def choosevendortemplate(request):
    if request.user.is_Vendor:
        vendor = VendorAccount.objects.get(email=request.user.email)

        if request.method == 'POST':
            tname = request.POST.get('tname')
            vendor.template = tname
            vendor.save()

            # vendor.update(corousel1="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel2="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel3="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel4="media/shop/1/template/unnamed_KlxQMYr.jpg",
            #               corousel5="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel6="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel7="media/shop/1/template/unnamed_KlxQMYr.jpg", logo=logo)
            msg = "Template updated Successfully"
            return render(request, "account/choose_template_vendor.html", {'msg': msg, 'vendor': vendor})
        else:
            return render(request, "account/choose_template_vendor.html", {'vendor': vendor})
    else:
        return render(request, "general/unauthorized.html")


@login_required(login_url="../login")
def customise_vendor_template(request):
    if request.user.is_Vendor:
        vendor = VendorAccount.objects.get(email=request.user.email)

        if request.method == 'POST':
            tname = request.POST.get('tname')
            corousel1 = request.FILES.get('corousel1')
            corousel2 = request.FILES.get('corousel2')
            corousel3 = request.FILES.get('corousel3')
            corousel4 = request.FILES.get('corousel4')
            corousel5 = request.FILES.get('corousel5')
            corousel6 = request.FILES.get('corousel6')
            corousel7 = request.FILES.get('corousel7')
            corousel8 = request.FILES.get('corousel8')
            logo = request.FILES.get('logo')

            if logo is not None:
                default_storage.delete(str(vendor.logo))
                vendor.logo = logo
            if corousel1 is not None:
                default_storage.delete(str(vendor.corousel1))
                vendor.corousel1 = corousel1
            if corousel2 is not None:
                default_storage.delete(str(vendor.corousel2))
                vendor.corousel2 = corousel2
            if corousel3 is not None:
                default_storage.delete(str(vendor.corousel3))
                vendor.corousel3 = corousel3
            if corousel4 is not None:
                default_storage.delete(str(vendor.corousel4))
                vendor.corousel4 = corousel4
            if corousel5 is not None:
                default_storage.delete(str(vendor.corousel5))
                vendor.corousel5 = corousel5
            if corousel6 is not None:
                default_storage.delete(str(vendor.corousel6))
                vendor.corousel6 = corousel6
            if corousel7 is not None:
                default_storage.delete(str(vendor.corousel7))
                vendor.corousel7 = corousel7
            vendor.save()

            # vendor.update(corousel1="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel2="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel3="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel4="media/shop/1/template/unnamed_KlxQMYr.jpg",
            #               corousel5="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel6="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel7="media/shop/1/template/unnamed_KlxQMYr.jpg", logo=logo)
            msg = "Template updated Successfully"
            return render(request, "account/customise_template_vendor.html.html", {'msg': msg, 'vendor': vendor})
        else:
            return render(request, "account/customise_template_vendor.html", {'vendor': vendor})
    else:
        return render(request, "general/unauthorized.html")


@login_required(login_url="../login")
def choosebloggertemplate(request):
    if request.user.is_Blogger:
        blogger = BloggerAccount.objects.get(email=request.user.email)

        if request.method == 'POST':
            tname = request.POST.get('tname')
            blogger.template = tname
            blogger.save()
            # vendor.update(corousel1="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel2="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel3="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel4="media/shop/1/template/unnamed_KlxQMYr.jpg",
            #               corousel5="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel6="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel7="media/shop/1/template/unnamed_KlxQMYr.jpg", logo=logo)
            msg = "Template updated Successfully"
            return render(request, "account/choose_template_blog.html", {'msg': msg, 'blogger': blogger})
        else:
            return render(request, "account/choose_template_blog.html", {'blogger': blogger})
    else:
        return render(request, "general/unauthorized.html")


@login_required(login_url="../login")
def customise_blogger_template(request):
    if request.user.is_Vendor:
        blogger = BloggerAccount.objects.get(email=request.user.email)

        if request.method == 'POST':
            tname = request.POST.get('tname')
            corousel1 = request.FILES.get('corousel1')
            corousel2 = request.FILES.get('corousel2')
            corousel3 = request.FILES.get('corousel3')
            corousel4 = request.FILES.get('corousel4')
            corousel5 = request.FILES.get('corousel5')
            corousel6 = request.FILES.get('corousel6')
            corousel7 = request.FILES.get('corousel7')
            corousel8 = request.FILES.get('corousel8')
            logo = request.FILES.get('logo')

            if logo is not None:
                default_storage.delete(str(blogger.logo))
                blogger.logo = logo
            if corousel1 is not None:
                default_storage.delete(str(blogger.corousel1))
                blogger.corousel1 = corousel1
            if corousel2 is not None:
                default_storage.delete(str(blogger.corousel2))
                blogger.corousel2 = corousel2
            if corousel3 is not None:
                default_storage.delete(str(blogger.corousel3))
                blogger.corousel3 = corousel3
            if corousel4 is not None:
                default_storage.delete(str(blogger.corousel4))
                blogger.corousel4 = corousel4
            if corousel5 is not None:
                default_storage.delete(str(blogger.corousel5))
                blogger.corousel5 = corousel5
            if corousel6 is not None:
                default_storage.delete(str(blogger.corousel6))
                blogger.corousel6 = corousel6
            if corousel7 is not None:
                default_storage.delete(str(blogger.corousel7))
                blogger.corousel7 = corousel7
            blogger.save()

            # vendor.update(corousel1="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel2="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel3="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel4="media/shop/1/template/unnamed_KlxQMYr.jpg",
            #               corousel5="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel6="media/shop/1/template/unnamed_KlxQMYr.jpg", corousel7="media/shop/1/template/unnamed_KlxQMYr.jpg", logo=logo)
            msg = "Template updated Successfully"
            return render(request, "account/customise_template_blog.html", {'msg': msg, 'blogger': blogger})
        else:
            return render(request, "account/customise_template_blog.html", {'blogger': blogger})
    else:
        return render(request, "general/unauthorized.html")


@login_required(login_url="../login")
def account_view(request):
    # if not request.user.is_authenticated:
    #     return redirect("../login")
    global msg

    context = {"name": request.user.name, "email": request.user.email, "contact_number": request.user.contact_number,
               "msg": msg}
    if request.user.is_Vendor:
        vendor = VendorAccount.objects.get(email=request.user.email)
    else:
        vendor = None
    if request.POST:
        name = request.POST['name']
        contact_number = request.POST.get('contact_number')
        email = request.POST['email']
        password = request.POST.get('password')
        user = authenticate(email=request.user.email, password=password)
        if user:
            userid = request.user.id
            Account.objects.filter(id=userid).update(name=name, email=email, contact_number=contact_number)

            context = {"name": name, "email": email, "contact_number": contact_number, "msg": "",}
        else:
            msg = "Wrong Password"
            context["msg"] = msg

    context["vendor"]=vendor
    print(context)
    return render(request, 'account/profile.html', context)


@login_required(login_url="../login")
def changepassword(request):
    global msg
    password = request.POST.get('password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')
    user = authenticate(email=request.user.email, password=password)
    if user:
        if new_password == confirm_password:
            userid = request.user.id
            u = Account.objects.get(id=userid)
            u.set_password(new_password)
            u.save()
            Account.objects.filter(id=userid).update(viewpass=new_password, )
            msg = "Password Changed"
        else:
            msg = "new password not match with confirm password"
    else:
        msg = "Wrong password"
    return redirect("../account")

@login_required(login_url="../login")
def getKYC(request):
    if request.method == 'POST':
        aadhaar = request.POST['aadhaar']
        pan = request.POST['pan']
        companypan = request.POST['companypan']
        aadhaarImage = request.POST['aadhaarImage']
        panImage = request.POST['panImage']
        companyPanImage = request.POST['companypanImage']
        VendorAccount.aadhaar_card = aadhaar
        VendorAccount.pan = pan
        VendorAccount.companypan = companypan
        VendorAccount.aadhaar_image = aadhaarImage
        VendorAccount.pan_image = panImage
        VendorAccount.companypan_image = companyPanImage
        
    else:
        return render(request,"account/kyc.html")    

def check(request):

    return HttpResponse("helli")

