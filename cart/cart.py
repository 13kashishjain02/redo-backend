from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Cartdata
from . import views
from account import views
qty=00

class Cart(object):
    
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product,size,username, quantity=1, action=None):
        """
            Add a product to the cart or update its quantity.
        """
        global qty
        id = product.id
        newItem = True
        if str(product.id) not in self.cart.keys():
            
            #username = views.usermail()
            orders_temp = Cartdata.objects.filter(username=username)
            orders_temp = orders_temp.filter(product_id=1)
            orders = orders_temp.values()
            if orders:
                qty=orders[0]
                qty=qty['qty']
            else:
                qty=1

            self.cart[product.id] = {
                'userid': self.request.user.id,
                'product_id': id,
                'name': product.name,
                'quantity': qty,
                'size': size,
                'price': str(product.price),
                'image': product.image.url
            }
            
            
        else:
            newItem = True

            for key, value in self.cart.items():
                if key == str(product.id):
                    value['quantity']=qty
                    value['quantity'] = value['quantity'] + 1
                    
                    qty=value['quantity']
                    newItem = False
                    self.save()
                    break
            if newItem == True:

                self.cart[product.id] = {
                    'userid': self.request,
                    'product_id': product.id,
                    'name': product.name,
                    'size': size,
                    'quantity': qty,
                    'price': str(product.price),
                    'image': product.image.url
                }

        self.save()
        views.savedata(product.id,qty,size,username)
        

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product,size,username):
        global qty
        for key, value in self.cart.items():
            if key == str(product.id):
                # username = views.usermail()
                #username = "jain@jain.com"
                orders_temp = Cartdata.objects.filter(username=username)
                orders_temp = orders_temp.filter(product_id=1)
                orders = orders_temp.values()
                if orders:
                    qty=orders[0]
                    qty=qty['qty']
                else:
                    qty=1

                value['quantity'] = value['quantity'] - 1
                qty=value['quantity']
                if(value['quantity'] < 1):
                    return redirect('cart:cart_detail')
                self.save()
                break
            else:
                print("Something Wrong")

        views.savedata(product.id,qty,size,username)

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
