from django.shortcuts import render
from shop.models import Product, SubCategory2,Cart
from account.models import VendorAccount
from django.http import HttpResponseRedirect, HttpResponse
from .serializers import CartSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

@csrf_exempt
@api_view(['POST','GET',])
# @permission_classes([])
@permission_classes([IsAuthenticated])
def cart_api(request):
    if request.method=="GET":
        if id is None:
            data=Cart.objects.all()
            serializer=CartCommentSerializer(data,many=True)
            return Response(serializer.data)

        else:
            # debate=Debate.objects.get(pk=id)
            data=Cart.objects.filter(pk=id)
            serializer=CartSerializer(data,many=True)
            return Response(serializer.data)


    if request.method=='POST':
        data=request.data
        try:
            cart = Cart.objects.get(user=request.user)
            counter=0
            for i in cart.cartdata:
                if i["product_id"]==data["product_id"]:
                    check=1
                    temp=i
                    break
                else:
                    check=0
                counter+=1
            if check==1:
                if temp["size"] == data["size"]:
                    cart.cartdata[counter]["qty"] = data["qty"]
                    cart.save()
                else:
                    cart.cartdata.append(data)
                    cart.save()
            elif check==0:
                cart.cartdata.append(data)
                cart.save()
        except ObjectDoesNotExist:
            data = [data]
            cart = Cart.objects.create(user=request.user, cartdata=data)
            cart.save()

        return Response({'DATA CREATED'})
        # return Response(serializer.errors)
