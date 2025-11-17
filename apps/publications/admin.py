from django.contrib import admin
from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'company', 'status', 'views_count', 'published_at', 'created_at']
    list_filter = ['status', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'author__email', 'company__name', 'tags']
    ordering = ['-created_at']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('author', 'company', 'title', 'slug', 'status')
        }),
        ('Contenu', {
            'fields': ('content', 'image', 'tags')
        }),
        ('Statistiques', {
            'fields': ('views_count', 'published_at')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'slug']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.author = request.user
        super().save_model(request, obj, form, change)