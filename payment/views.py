import requests
from django.shortcuts import render
from django.template import RequestContext
from django.template.context_processors import csrf

from paywix import payu
import hashlib
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from paywix.payu import Payu

from PayTm import Checksum2

import json
from django.http import HttpResponse
from twilio.rest import Client
import datetime
import random

# import functions and models
from shop import views
from shop.models import Order,Cart

username = ""


def uniquecode():
    # this function returns a unique code everytime it is called
    x = datetime.datetime.now()
    alphabets = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z',
                 'X', 'C', 'V', 'B', 'N', 'M']
    uniquecode = str(x.day) + str(x.month) + str(x.year)[2:] + random.choice(alphabets) + random.choice(
        alphabets) + str(x.time())[0:2] + str(x.time())[3:5]
    return uniquecode


twilio_config = {
    "account_sid": 'AC58aae686ada0a42728e123cfee24cd5b',
    "auth_token": '3808a360990a19b3a716a6e898d765fb',
}


# --------------------------------------------------------------------
# --------------------------------------------------------------------
# PAYU GATEWAY
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# pip install paywix
# --------------------------------
payu_config = {
        "merchant_key": "iGQDCdjy",
        "merchant_salt": "xVTgC3Fy51",
        "mode": "test",
        "success_url": "http://127.0.0.1:8000/payusuccess/",
        "failure_url": "http://127.0.0.1:8000/payufailure/"
    }
def payucheckout(request,amount):


    merchant_key = payu_config.get('merchant_key')
    merchant_salt = payu_config.get('merchant_salt')
    surl = payu_config.get('success_url')
    furl = payu_config.get('failure_url')
    mode = payu_config.get('mode')

    # Create payu instance
    payu = Payu(merchant_key, merchant_salt, surl, furl, mode)
    userdata = request.user
    data = {
        'amount': str(amount), 'firstname': userdata.name,
        'email': userdata.email,
        'phone': userdata.contact_number, 'productinfo': 'test', 'lastname': 'test', 'address1': 'test',
        'address2': 'test', 'city': 'test', 'state': 'test', 'country': 'test',
        'zipcode': 'tes', 'udf1': '', 'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
    }
    # Make sure the transaction ID is unique
    txnid = uniquecode()
    data.update({"txnid": txnid})
    payu_data = payu.transaction(**data)
    return render(request, "payment/payucheckout.html", {"posted": payu_data})


@csrf_protect
@csrf_exempt
def payusuccess(request):
    # data = {k: v[0] for k, v in dict(request.POST).items()}
    # response = payu.verify_transaction(data)
    c = {}
    c.update(csrf(request))
    status = request.POST.get("status")
    firstname = request.POST.get("firstname")
    amount = request.POST.get("amount")
    txnid = request.POST.get("txnid")
    posted_hash = request.POST.get("hash")
    key = request.POST.get("key")
    productinfo = request.POST.get("productinfo")
    email = request.POST.get("email")
    salt = "GQs7yium"
    try:
        additionalCharges = request.POST.get("additionalCharges")
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if hashh != posted_hash:
        print
        "Invalid Transaction. Please try again"
    else:
        print
        "Thank You. Your order status is ", status
        print
        "Your Transaction ID for this transaction is ", txnid
        print
        "We have received a payment of Rs. ", amount, ". Your order will soon be shipped."
    # if status=="success":
    #     print("helollllooo",request.user.email)
    #     Cart.objects.filter(user=request.user).delete()
    #     print("jkadshfjksah")
    #     order = Order.objects.filter(user=request.user)
    #     print(order,order[0],order[0].date)
    #     order.transaction_id = txnid
    #     order.status = 'placed'
    return render(request, 'payment/payusuccess.html', {"txnid": txnid, "status": status, "amount": amount})


@csrf_protect
@csrf_exempt
def payufailure(request):
    c = {}
    c.update(csrf(request))
    status = request.POST.get("status")
    firstname = request.POST.get("firstname")
    amount = request.POST.get("amount")
    txnid = request.POST.get("txnid")
    posted_hash = request.POST.get("hash")
    key = request.POST.get("key")
    productinfo = request.POST.get("productinfo")
    email = request.POST.get("email")
    salt = ""
    try:
        additionalCharges = request.POST.get("additionalCharges")
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if (hashh != posted_hash):
        print
        "Invalid Transaction. Please try again"
    else:
        print
        "Thank You. Your order status is ", status
        print
        "Your Transaction ID for this transaction is ", txnid
        print
        "We have received a payment of Rs. ", amount, ". Your order will soon be shipped."
    return render("payment/payufailure.html", RequestContext(request, c))


def payusubscription(request):
    data = {"client_id": "ccbb70745faad9c06092bb5c79bfd919b6f45fd454f34619d83920893e90ae6b",
            "grant_type": "password",
            "username": "kashish.iitdelhi@gmail.com",
            "password": "Kashish2002@",
            "scope": "create_payout_transactions",
            }
    url = "https://accounts.payu.in/oauth/token"
    # url="https://uat-accounts.payu.in/oauth/token"
    response = requests.post(url, data=data).json()
    print(response)
    print(response.get('access_token'))
    subdata={
        "merchant_id":payu_config.get('merchant_key'),
        "access_token":response.get('access_token'),
        "amount": "100",
        "frequency": "1",
        "frequencyType":"months",
        "surl": "http://127.0.0.1:8000",
        "furl":"http://127.0.0.1:8000"
    }
    url2="https://www.payumoney.com/subscriptions/subscriptionPlans/createDynamicPlan"
    response2 = requests.post(url2, data=data,headers={"Content-type": "application/json"}).json()
    print(response2)
    # return render(request, "payment/payusub.html", {"sub": subdata})
    return HttpResponse("hello world")


# --------------------------------------------------------------------
# --------------------------------------------------------------------
# PAYTM GATEWAY
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# pip install pycryptodome
# --------------------------------

def paytmcheckout(request):
    MERCHANT_KEY = 'Ujzdeai9L@l%#6!o'
    global username
    username = request.user.email
    a, total = views.olist(username)

    txn_amount = str(total)
    param_dict = {

        'MID': 'vgADHx05412495283112',
        'ORDER_ID': uniquecode(),
        'TXN_AMOUNT': txn_amount,
        'CUST_ID': username,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/paytmhandlerequest/',

    }
    param_dict['CHECKSUMHASH'] = Checksum2.generateSignature(param_dict, MERCHANT_KEY)
    return render(request, 'payment/paytm.html', {'param_dict': param_dict})


@csrf_exempt
def paytmhandlerequest(request):
    # paytm will send you post request here
    MERCHANT_KEY = 'Ujzdeai9L@l%#6!o'
    form = request.POST

    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]

        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum2.verifySignature(response_dict, MERCHANT_KEY, checksum)

    if verify:
        if response_dict['RESPCODE'] == '01':
            global username
            a, total = views.olist(username)
            order_list = ""
            for i in a:
                order_list = order_list + "[ product id : " + str(i["product_id"]) + ", vendor : " + i[
                    "vendor"] + ", price : " + str(i["price"]) + ", qty : " + str(i["qty"]) + "]"

            # twilio message

            client = Client(twilio_config.get('account_sid'), twilio_config.get('auth_token'))

            message = client.messages \
                .create(
                body="a order has been placed " + order_list,
                from_='+14159696324',
                to='+916264843506'
            )

            # print(message.sid)
            orders_temp = Cartdata.objects.filter(username=username)
            print(orders_temp)
            orders_temp.delete()
            return render(request, 'payment/paytmpaymentstatus.html', {'response': response_dict})

        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'payment/paytmpaymentstatus.html', {'response': response_dict})
