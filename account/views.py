from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from .models import Account, VendorAccount, BloggerAccount
# from cart.models import Cartdata
from django.contrib.auth.models import auth, User
from django.contrib.auth import logout, login, authenticate
from account.forms import AccountAuthenticationForm
import requests
import json
from datetime import date
from django.core.files.storage import default_storage
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum2
from django.http import HttpResponseRedirect, HttpResponse
# ---------------------------------------------------
# GLOBAL VARIABLES
# ---------------------------------------------------
MERCHANT_KEY = 'Ujzdeai9L@l%#6!o'
usenamee = "notdefined@gmail.com"
subsId = ""
shopname = ""
shop_add = ""
plan = ""
vendorname = ""
vendoremail = ""
mobile = ""
promocode = ""
code = {"starter10": 10, "economic20": 20, "advanced100": 100, "starter20": 20, "economic30": 30, "advanced80": 80,
        "starter15": 15, "economic40": 40, "advanced150": 150}
gst = ""
msg = ""


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def usermail():
    global usernamee
    usernaam = usernamee
    # usernaam = "jain@jain.com"
    return usernaam



# -----------------------------------------------------------------------

def userregister(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact_number = int(request.POST['mobile'])
        email = request.POST['email']
        password = request.POST.get('password')
        try:
            user = Account.objects.create_user(
                name=name, email=email, password=password, contact_number=contact_number, viewpass=password
            )
            user.save()
            print("1")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            msg = "User Registration Successful"
            print("1")
            return redirect("../")
        except IntegrityError as e:
            msg = email + " is already registered,if you think there is a issue please contact us at 6264843506"
            print("3")
            return render(request, "account/register.html", {'msg': msg})
        except Exception as e:
            print(e)
            print("2")
        # return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return render(request, "account/register.html")


def userlogin(request):
    msg = ""
    user = request.user
    if user.is_authenticated:
        return redirect("../")
    else:
        if request.POST:
                email = request.POST.get('email')
                password = request.POST.get('password')
                user = authenticate(email=email, password=password)
                if user:
                    login(request, user)
                    request.user = user
                    next = request.POST.get('next', '../')
                    if next == "":
                        next="../"
                    return redirect(next)
                    # return redirect('../')
                else:
                    msg = "invalid Email or password"
        else:
            form = AccountAuthenticationForm()
        return render(request, 'account/login.html', {"form": form, "msg": msg})
    # username=BaseUserManager.normalize_email(username)

    context['login form'] = form
    print("context :", context)
    return render(request, 'account/register.html', context)


@login_required(login_url="../login")
def logoutuser(request):
    logout(request)
    return redirect("../")


@login_required(login_url="../login")
def vendorregister(request):
    global shopname
    global shop_add
    global plan
    global vendorname
    global vendoremail
    global mobile
    global promocode
    global gst

    if request.method == 'POST':
        email = request.user.email
        shop_number = request.POST.get('shop_number')
        shopname = request.POST.get('shopname').lower()
        gst = request.POST.get('gst')
        shop_add_flat = request.POST['shop_add_flat']
        shop_add_city = request.POST['shop_add_city']
        shop_add_state = request.POST['shop_add_state']
        shop_add_pincode = str(request.POST.get('shop_add_pincode'))
        # shop_add = shop_add_flat + "," + shop_add_city + "," + shop_add_state + "," + shop_add_pincode
        plan = request.POST['plan']
        subscription_amount = 50
        vendor = Account.objects.get(email=email)
        vendor.is_Vendor = True
        vendor.save()
        promocode = request.POST.get('promocode')

        try:
            user = VendorAccount.objects.create(
                shop_name=shopname, shop_number=shop_number, shop_add=shop_add_flat, city=shop_add_city,
                state=shop_add_state, plan=plan, gst=gst, vendor=vendor,
                subscripton_amount=subscription_amount, email=email)
            user.save()

        except IntegrityError as e:
            e = str(e)
            if e == "UNIQUE constraint failed: account_vendoraccount.shop_name":
                shopname = shopname + "#" + vendor.name[2:5]

                user = VendorAccount.objects.create(
                    shop_name=shopname, shop_number=shop_number, shop_add=shop_add, plan=plan, gst=gst, vendor=vendor,
                    subscripton_amount=subscription_amount, email=email)
                user.save()
            else:
                msg = "vendor already registered,if you think there is a issue please contact us at 6264843506"
                return render(request, "account/vendorregister.html", {'msg': msg})

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
        msg = "Vendor Registration Successful"
        return render(request, 'general/index.html', {'msg': msg})
    else:
        return render(request, "account/vendorregister.html")


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
    if request.POST:
        name = request.POST['name']
        contact_number = request.POST.get('contact_number')
        email = request.POST['email']
        password = request.POST.get('password')
        user = authenticate(email=request.user.email, password=password)
        if user:
            userid = request.user.id
            Account.objects.filter(id=userid).update(name=name, email=email, contact_number=contact_number)
            context = {"name": name, "email": email, "contact_number": contact_number, "msg": ""}
        else:
            msg = "Wrong Password"
            context["msg"] = msg
    return render(request, 'account/myaccount.html', context)


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
            msg = "new password does not match with confirm password"
    else:
        msg = "Wrong password"
    return redirect("../account")


def subscription(request):
    custId = "order" + str(request.user.id)

    global plan
    global promocode
    global code

    value = 00
    if plan == "starter":
        value = 20
    elif plan == "economic":
        value = 50
    elif plan == "advanced":
        value = 200
    if value == 00:
        value = 50
    # value=10
    for i in code:
        if promocode == i:
            value = code[i]

    value = str(value)
    paytmParams = dict()

    paytmParams["body"] = {
        "requestType": "NATIVE_SUBSCRIPTION",
        "mid": "vgADHx05412495283112",
        "websiteName": "WEBSTAGING",
        "orderId": custId,
        "callbackUrl": "http://127.0.0.1:8000/handlesubscription/",
        "subscriptionAmountType": "FIX",
        "subscriptionStartDate": str(date.today()),
        "autoRenewal": True,
        "subscriptionGraceDays": "1",
        "subscriptionFrequency": "1",
        "subscriptionFrequencyUnit": "MONTH",
        "subscriptionExpiryDate": "2031-05-20",
        "subscriptionEnableRetry": "1",
        "txnAmount": {
            "value": value,
            "currency": "INR",
        },
        "userInfo": {
            "custId": custId,
        },
    }

    checksum = Checksum2.generateSignature(json.dumps(paytmParams["body"]), MERCHANT_KEY)
    print("checksum: :", checksum)
    paytmParams["head"] = {
        "signature": checksum
    }
    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/subscription/create?mid=vgADHx05412495283112&orderId= " + \
          paytmParams["body"]["orderId"]

    # for Production
    # url = "https://securegw.paytm.in/subscription/create?mid=vgADHx05412495283112&orderId=ORDERID_98765"

    response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
    print(response)
    global subsId
    subsId = response["body"]["subscriptionId"]
    return render(request, 'account/paytm.html', {'response': response, 'orderId': paytmParams["body"]["orderId"]})


@csrf_exempt
def handlesubscription(request):
    global subsId
    global shopname
    global shop_add
    global plan
    global vendorname
    global vendoremail
    global mobile
    global gst

    paytmParams = dict()

    paytmParams["body"] = {
        "mid": "vgADHx05412495283112",
        "subsId": subsId
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = Checksum2.generateSignature(json.dumps(paytmParams["body"]), MERCHANT_KEY)

    paytmParams["head"] = {
        "tokenType": "AES",
        "signature": checksum
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/subscription/checkStatus"

    # for Production
    # url = "https://securegw.paytm.in/subscription/checkStatus"

    response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
    user = VendorAccount.objects.create_vendor(
        name=vendorname, email=vendoremail, shop_name=shopname, contact_number=mobile, shop_add=shop_add, plan=plan
        , gst=gst, user=request.user)
    user.save()
    # user = VendorAccount.objects.create_vendor(
    #     name="vendorname", email="kashish@gmail.com", shop_name="shopname", contact_number=6264843506, shop_add="shop_add", plan="plan",
    #     gst=gst, user=request.user)
    # user.save()
    return redirect("../")



def check(request):

    return HttpResponse("helli")