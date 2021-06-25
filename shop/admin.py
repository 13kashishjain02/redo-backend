from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Product, Order,MyModel,PropertyImage,Property,Category,SubCategory2,SubCategory1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'name', 'pub_date',)
    search_fields = ('id', 'name', 'category.name', 'subcategory.name', 'price', 'product_for')
    readonly_fields = ()
    ordering = ('pub_date',)
    filter_horizontal = ()
    list_filter = ()


admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(MyModel)
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3

class PropertyAdmin(admin.ModelAdmin):
    inlines = [ PropertyImageInline, ]

admin.site.register(Property, PropertyAdmin)
admin.site.register(Category)
admin.site.register(SubCategory1)
admin.site.register(SubCategory2)