from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'cfe_number', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'cfe_number', 'user__email']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('user', 'name', 'cfe_number', 'is_active')
        }),
        ('Coordonnées', {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']