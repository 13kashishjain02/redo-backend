from shop.models import Product
from rest_framework import routers, serializers, viewsets


class ProductSerializer(serializers.ModelSerializer):
    subcategory1 = serializers.SerializerMethodField('get_subcategory1')
    category = serializers.SerializerMethodField('get_category')

    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ['vendor']

    def get_subcategory1(self, obj):
        subcategory1 = obj.subcategory2.subcategory1.name
        return subcategory1

    def get_category(self, obj):
        category = obj.subcategory2.subcategory1.category.name
        return category


