from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Cartdata
from account import views

# Create your views here.
def savecartdata(product_id,qty,sizee):
	
	username = views.usermail()
	#username = "jain@jain.com"
	catprods = Cartdata.objects.values('username', 'product_id')
	for sub in catprods: 
		if sub['username'] == username and sub['product_id'] == product_id: 
			instance = Cartdata.objects.filter(product_id=product_id)
			instance = instance.filter(username=username)
			instance.delete()	
			
			
				
	#if Cartdata.objects.get(username=username):
	#	if Cartdata.objects.get(product_id=product_id):
	#		instance = Cartdata.objects.get(product_id=product_id)
	#		instance.delete()
	
	p_order = Cartdata.objects.create(username=username,product_id=product_id,qty=qty,size=sizee)
	p_order.save()
	