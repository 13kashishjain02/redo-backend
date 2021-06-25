from django.contrib import admin
from payment.models import Coupons


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code',)
    search_fields = ('code',)
    readonly_fields = ()
    ordering = ('code',)
    filter_horizontal = ()
    list_filter = ()

admin.site.register(Coupons, CouponAdmin)