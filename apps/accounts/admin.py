from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'account_type', 'is_active', 'is_staff', 'created_at']
    list_filter = ['account_type', 'is_active', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['email', 'first_name', 'last_name', 'company_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'address')
        }),
        ('Type de compte', {
            'fields': ('account_type', 'company_name', 'cfe_number')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'account_type'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']