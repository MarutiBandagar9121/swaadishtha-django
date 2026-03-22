from django.contrib import admin

from .models import Order
from .models import OrderProduct
from .models import OrderAddress
from .models import PaymentInfo
from .models import InvoiceNumbering
from .models import Invoice

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'order_status', 'created_at','updated_at']
    list_filter = ['order_status', 'created_at', 'updated_at']
    search_fields = ['id', 'user__email', 'total_amount', 'order_status']

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id','order','product_variant','product_rate','product_qty', 'subtotal','created_at', 'updated_at']
    list_filter = ['order', 'product_variant', 'created_at', 'updated_at']
    search_fields = ['id', 'order__id', 'product_variant__sku', 'product_rate', 'product_qty', 'subtotal']

@admin.register(OrderAddress)
class OrderAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'address_type', 'address_line1', 'address_line2', 'city', 'state', 'country', 'postal_code', 'created_at', 'updated_at']
    list_filter = ['order', 'address_type', 'created_at', 'updated_at']
    search_fields = ['id', 'order__id', 'address_type', 'address_line1', 'address_line2', 'city', 'state', 'country', 'postal_code']

@admin.register(PaymentInfo)
class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'payment_gateway', 'payment_method', 'amount', 'payment_status', 'gateway_transaction_id', 'created_at', 'updated_at']
    list_filter = ['order', 'payment_gateway', 'payment_method', 'payment_status', 'created_at', 'updated_at']
    search_fields = ['id', 'order__id', 'payment_gateway', 'payment_method', 'amount', 'payment_status', 'gateway_transaction_id']

@admin.register(InvoiceNumbering)
class InvoiceNumberingAdmin(admin.ModelAdmin):
    list_display = ['id', 'financial_year', 'invoice_prefix', 'last_invoice_number']
    list_filter = ['financial_year', 'invoice_prefix']
    search_fields = ['id', 'financial_year', 'invoice_prefix', 'last_invoice_number']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_number', 'total_amount', 'taxable_amount', 'sgst', 'cgst', 'igst', 'created_at', 'updated_at']
    list_filter = ['order', 'invoice_number', 'created_at', 'updated_at']
    search_fields = ['order__id', 'invoice_number', 'total_amount', 'taxable_amount', 'sgst', 'cgst', 'igst']