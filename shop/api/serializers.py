from shop.models import Product
from rest_framework import routers, serializers, viewsets


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ['vendor']



