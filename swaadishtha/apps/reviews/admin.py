from django.contrib import admin

from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'status', 'created_at']
    search_fields = ['user__email', 'product__name', 'comment']
    list_filter = ['status', 'rating', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
