from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Product, Order,Category,SubCategory2,SubCategory1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'name', 'pub_date',)
    # subcategory2__name works as subcategory2.name
    search_fields = ('id', 'name',  'subcategory2__name','subcategory2__subcategory1__name', 'price', 'product_for')
    readonly_fields = ()
    ordering = ('pub_date',)
    filter_horizontal = ()
    list_filter = ()


admin.site.register(Product, ProductAdmin)
admin.site.register(Order)

admin.site.register(Category)
admin.site.register(SubCategory1)
admin.site.register(SubCategory2)