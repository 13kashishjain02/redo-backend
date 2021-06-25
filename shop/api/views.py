from django.shortcuts import render
from shop.models import Product,SubCategory2
from django.http import HttpResponseRedirect, HttpResponse
from .serializers import ProductSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.utils import IntegrityError
from django.urls import reverse


@csrf_exempt
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def Product_api(request, id=None):
    if request.method == "GET":
        if id is None:
            data = Product.objects.all()
            serializer = ProductSerializer(data, many=True)
            # print("hellloooo",serializer.data[0])
            for i in serializer.data:
                sub = SubCategory2.objects.get(id=i['subcategory2'])
                i['subcategory2'] = sub.name
                i['subcategory1'] = sub.subcategory1.name
                i['category'] = sub.subcategory1.category.name

            return Response(serializer.data)

        else:
            # data = Product.objects.get(pk=id)
            data = Product.objects.filter(pk=id)
            serializer = ProductSerializer(data, many=True)
            print(data[0])
            serializer.data[0]['subcategory2']=data[0].subcategory2.name
            serializer.data[0]['subcategory1'] = data[0].subcategory2.subcategory1.name
            serializer.data[0]['category'] = data[0].subcategory2.subcategory1.category.name
            # print(serializer.data)
            return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        # print(serializer.data)
        if serializer.is_valid():
            comment = serializer.data
            data = Product.objects.get(pk=id)
            data.comments.append(comment["comments"])
            data.save()

            # serializer.save()
            return Response({'msg', 'DATA CREATED'})
        return Response(serializer.errors)

    if request.method == 'PUT':
        data = Product.objects.get(pk=id)
        serializer = ProductSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print("PUT data", serializer.data)
            return Response({'msg', 'Data Updated'})
        return Response(serializer.errors)

    if request.method == 'DELETE':
        data = Product.objects.get(pk=id)
        data.delete()
        return Response({'msg': 'data deleted'})
