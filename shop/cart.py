# from shop.models import Product, SubCategory2,Cart
# from django.shortcuts import render,redirect
# from django.core.exceptions import ObjectDoesNotExist
# from account.models import VendorAccount
# from django.http import HttpResponseRedirect, HttpResponse
# import math

# def add_to_cart(request):
#     pass

# def mycart(request):
#     try:
#         cart = Cart.objects.get(user=request.user)
#         data=cart.cartdata
#         counter=0
#         total=0
#         final_total=0
#         for i in data:
#             print("i[product_id]",i["product_id"])
#             product=Product.objects.get(id=i["product_id"])
#             data[counter]["mrp"]=product.mrp
#             data[counter]["special_price"] = product.special_price
#             data[counter]["our_price"] = product.our_price
#             data[counter]["name"] = product.name
#             data[counter]["image"] = product.image
#             data[counter]["slug"] = product.slug
#             # data[counter]["discount"] = math.floor(100-(product.special_price/product.mrp)*100)
#             if product.our_price:
#                 total = total + product.our_price*int(data[counter]["qty"])
#             elif product.special_price:
#                 total = total + product.special_price*int(data[counter]["qty"])
#             else:
#                 total = total + product.mrp*int(data[counter]["qty"])
#             counter+=1
#         final_total=total+60 #60 for delivery
#         print("cart",total)
#         return render(request, 'shop/mycart.html', {'cart': data,'total':total,'final_total':final_total})
#     except Exception as e:
#         print(e)
#         return render(request, 'shop/mycart.html')

# def addtocart(request):
#     product_id = request.POST["id"]
#     size = request.POST.get("size")
#     color = request.POST.get("color")
#     print(color)
#     qty = request.POST["qty"]
#     data={"size": size, "color": color, "qty": qty, "product_id": product_id}
#     print("data",data)
#     try:
#         print("1")
#         cart = Cart.objects.get(user=request.user)
#         counter = 0
#         for i in cart.cartdata:
#             if i["product_id"] == data["product_id"]:
#                 print("3")
#                 check = 1
#                 temp = i
#                 break
#             else:
#                 check = 0
#             counter += 1
#         if check == 1:
#             print("4")

#             if temp["size"] == data["size"] or temp["color"]==data["color"]:
#                 print("5")
#                 cart.cartdata[counter]["qty"] = data["qty"]
#                 cart.save()
#             else:
#                 print("6")
#                 cart.cartdata.append(data)
#                 cart.save()
#         elif check == 0:
#             print("5")

#             cart.cartdata.append(data)
#             cart.save()
#     except ObjectDoesNotExist:
#         print("2")
#         data = [data]
#         cart = Cart.objects.create(user=request.user, cartdata=data)
#         cart.save()
#     return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# def increaseqty(request):
#     product_id = request.GET.get("id")
#     print(request.GET)
#     try:
#         print(1)
#         cart = Cart.objects.get(user=request.user)
#         counter = 0
#         for i in cart.cartdata:
#             if i["product_id"] == product_id:
#                 check = 1
#                 temp = i
#                 break
#             else:
#                 check = 0
#             counter += 1
#         if check == 1:
#             print(1)
#             cart.cartdata[counter]["qty"] = int(cart.cartdata[counter]["qty"])+1
#             cart.save()

#     except ObjectDoesNotExist:
#         return HttpResponse("something went wrong")
#     return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

# def decreaseqty(request):
#     product_id = request.GET.get("id")
#     print(request.GET)
#     try:
#         print(1)
#         cart = Cart.objects.get(user=request.user)
#         counter = 0
#         for i in cart.cartdata:
#             if i["product_id"] == product_id:
#                 check = 1
#                 temp = i
#                 break
#             else:
#                 check = 0
#             counter += 1
#         if check == 1:
#             print(1)
#             cart.cartdata[counter]["qty"] = int(cart.cartdata[counter]["qty"])-1
#             cart.save()

#     except ObjectDoesNotExist:
#         return HttpResponse("something went wrong")
#     return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))