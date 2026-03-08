from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'whatsapp_number', 'email_verified', 'whatsapp_number_verified', 'created_at']
    search_fields = ['email', 'name', 'whatsapp_number']
    list_filter = ['email_verified', 'whatsapp_number_verified', 'created_at']
