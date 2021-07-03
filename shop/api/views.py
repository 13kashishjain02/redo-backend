from django.shortcuts import render
from shop.models import Product, SubCategory2
from account.models import VendorAccount
from django.http import HttpResponseRedirect, HttpResponse
from .serializers import ProductSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.db.utils import IntegrityError
from django.urls import reverse


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter


@csrf_exempt
@api_view(['GET',])
# @permission_classes([IsAuthenticated])
@permission_classes([])
def product_api(request, id=None):
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
            serializer.data[0]['subcategory2'] = data[0].subcategory2.name
            serializer.data[0]['subcategory1'] = data[0].subcategory2.subcategory1.name
            serializer.data[0]['category'] = data[0].subcategory2.subcategory1.category.name
            # print(serializer.data)
            return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        # print(serializer.data)
        if serializer.is_valid():
            data = serializer.data
            vendor = VendorAccount.objects.get(email=request.user.email)
            data["vendor"]=vendor
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


# Url:
#		1) list: https://<your-domain>/api/blog/list
#		2) pagination: http://<your-domain>/api/blog/list?page=2
#		3) search: http://<your-domain>/api/blog/list?search=mitch
#		4) ordering: http://<your-domain>/api/blog/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/blog/list?search=mitch&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>

@permission_classes((AllowAny, ))
class ApiProductListView(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	# authentication_classes = (TokenAuthentication,)
	# permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('name', 'subcategory2__name', 'desc')