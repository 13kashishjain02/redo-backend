from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Product, Order,Category,SubCategory2,SubCategory1,Wishlist,Cart,Variation


class ProductAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'name', 'pub_date','id')
    # subcategory2__name works as subcategory2.name
    search_fields = ('id', 'name',  'subcategory2__name','subcategory2__subcategory1__name', 'price', 'product_for')
    readonly_fields = ()
    ordering = ('pub_date',)
    filter_horizontal = ()
    list_filter = ()

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','date','id')
    search_fields = ('id', 'used__name',  'date')
    readonly_fields = ()
    ordering = ('date',)
    filter_horizontal = ()
    list_filter = ()


admin.site.register(Product, ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Wishlist)
admin.site.register(Variation)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(SubCategory1)
admin.site.register(SubCategory2)