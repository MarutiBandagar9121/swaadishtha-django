from django.contrib import admin

from .models import Product
from .models import ProductImage
from .models import Attribute
from .models import AttributeValue
from .models import ProductVariant
from .models import VariantImage

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','is_active', 'status', 'created_at', 'updated_at']
    list_filter =['is_active', 'status', 'created_at', 'updated_at']
    filter_horizontal = ['categories']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'alt_text','position']

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['id', 'attribute', 'value']

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'sku', 'price', 'stock', 'is_active', 'status']
    list_filter = ['is_active', 'status', 'created_at', 'updated_at']
    search_fields = ['sku', 'product__name']
    filter_horizontal = ['attribute_values']

@admin.register(VariantImage)
class VariantImageAdmin(admin.ModelAdmin):
    list_display = ['variant', 'image', 'alt_text', 'position']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['variant__sku', 'alt_text']