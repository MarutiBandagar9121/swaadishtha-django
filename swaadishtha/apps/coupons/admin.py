from django.contrib import admin

from .models import Coupon
from .models import CouponUsage

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'valid_from_date', 'valid_upto_date', 'is_active', 'max_uses', 'current_uses')
    list_filter = ('discount_type', 'is_active', 'valid_from_date', 'valid_upto_date')
    search_fields = ('code',)
    date_hierarchy = 'valid_from_date'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'coupon__code')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')