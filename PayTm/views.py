from operator import add
from . import Checksum
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import VerifyPaytmResponse
import requests
from shop.models import Order,Cart
from account.models import Address
from shop.helpers import Total_MRP
from payment.models import Coupons

@csrf_exempt
def payment(request):
    order_id = Checksum.__id_generator__()
    code = 0
    if 'discount' in request.session:
        code = request.session['discount']
    total_mrp = Total_MRP(request)
    bill_amount = str(total_mrp - code)
    data_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
        'MOBILE_NO': '7405505665',
        'EMAIL': 'dhaval.savalia6@gmail.com',
        'CUST_ID': '123123',
        'ORDER_ID':order_id,
        'TXN_AMOUNT': bill_amount,
    } # This data should ideally come from database
    data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'comany_name': settings.PAYTM_COMPANY_NAME,
        'data_dict': data_dict
    }
    return render(request, 'payment/payment.html', context)

@csrf_exempt
def handle_response(request):
    try:
        form = request.POST
        response_dict = {}
        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                checksum = form[i]
        verify = Checksum.verify_checksum(response_dict,settings.PAYTM_MERCHANT_KEY,checksum)
        if verify:
            if response_dict['RESPCODE'] == '01':
                return redirect(f'/order-success/?TXNID={response_dict["TXNID"]}&RESPCODE={response_dict["RESPCODE"]}&TXNAMOUNT={response_dict["TXNAMOUNT"]}&ORDERID={response_dict["ORDERID"]}')             
    except:
        return redirect('/')
    return render(request,'payment/handle_response.html',{'response_dict':response_dict})


def order_success(request):
    try:
        response_dict = {}
        response_dict['TXNID'] = request.GET.get('TXNID')
        response_dict['RESPCODE'] = request.GET.get('RESPCODE')
        response_dict['TXNAMOUNT'] = request.GET.get('TXNAMOUNT')
        response_dict['ORDERID'] = request.GET.get('ORDERID')
        code = 0
        if 'discount' in request.session:
            code = request.session['discount']
        total_mrp = Total_MRP(request)
        total_amount = total_mrp - code
        address = Cart.objects.filter(user=request.user).first()
        order_list = []
        for i ,cart in enumerate(Cart.objects.filter(user=request.user)):
            if cart.product_variation is None:
                order_list.append({'product_id':cart.product.id,'price':cart.product.special_price,'quantity':cart.quantity,'size':'','type':'product'})
            else:
                order_list.append({'product_id':cart.product_variation.id,'price':cart.product_variation.special_price,'quantity':cart.quantity,'size':cart.size,'type':'variation'})
        Order.objects.create(
            user = request.user,
            transaction_id = response_dict['TXNID'],
            total = total_amount,
            contact_number = request.user.contact_number,
            address = address.address.address,
            state = address.address.state,
            city = address.address.city,
            zipcode = address.address.pincode,
            order_list = order_list
            )
        cart = Cart.objects.filter(user=request.user)
        for crt in cart:
            crt.delete()
        if 'coupon_code' in request.session:
            coupon = request.session['coupon_code']
            cupn = Coupons.objects.get(code=coupon)
            cupn.used = True
            cupn.save()
            del request.session['coupon_code']
    except:
        return redirect('/')
    return render(request,'payment/handle_response.html',{'response_dict':response_dict})